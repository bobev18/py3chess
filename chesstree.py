class Node:

    def __init__(self, path, move, depth_level, color):
        global nodecount
        nodecount += 1
        # self.predecessor = predecessor
        self.move = move
        self.path = path + '|' + move.notation
        # self.move_chain = path # this is used only for analysis 
        # self.move_chain += move.notation + '|'
        self.depth_level = depth_level
        self.color = color
        # if color == 'w': # switcing color to boolean ('w' = True, 'b' = False)
        if color:
            self.optimum = max
        else:
            self.optimum = min

        self.subnodes = []
        # self.scores = {}
        self.score = None

    def __repr__(self):
        return str([self.move, self.color, self.depth_level, self.path[1:]])

class Score:

    def __init__(self, value, optimal_cutoff_path):
        self.value = value
        self.optimal_cutoff_path = optimal_cutoff_path

class AI:

    def __init__(self, cutoff, game):
        self.game = game
        self.cutoff = cutoff
        # when starting the evaluate from outside use evaluate(node, node.depth_level + cutoff)
        self.draw_desire = -1 # can be in range [-1..1] where -1 means doesn't want draw, 1 means wants draw, and 0 = indifferent
        self.score_cache = {}

    def expand_node(self, node):
        # this method is called for nodes that are already executed onto the game object
        game_state = self.game.determine_game_state() # returns 'mate', 'stalemate', or list of all valid expansions
        if isinstance(game_state, list): # create new nodes
            node.subnodes = [  Node(node.path, z, node.depth_level + 1, not node.color) for z in game_state ]

    def score_node(self, node):
        undo = self.game.board.execute_move(node.move)
        game_state = self.game.determine_game_state()
        hash_ = ''.join(self.game.board.hashstate)
        try:
            score = self.score_cache[hash_]
        except KeyError:
            score = self.evaluator(game_state, self.game.board)
            self.score_cache[hash_] = score

        if isinstance(game_state, list): # create new nodes
            node.subnodes = [ Node(node.path, z, node.depth_level + 1, not node.color) for z in game_state ]

        self.game.board.undo_actions(undo)
        return score

    def evaluator(self, game_state, board):
        if game_state == 'mate':
            return 1000
        elif game_state == 'stalemate':
            print ('whaaaat')
            print(self.game.board)
            # raise Exception
            return 500*self.draw_desire
        else:
            # insert something with len(game_state) to consider number of moves available for the opponent
            return 3*len(board.white) - 3*len(board.black) + int(board.black_checked) - int(board.black_checked)

    def evaluate_position(self, by_color, cutoff_depth):
        game_state = self.game.determine_game_state()
        # print('gamestate', game_state)
        if isinstance(game_state, str):
            return evaluator(game_state, self.game.board)
        else:
            if by_color == 'w':
                oposite_color = 'b'
                color_optimum = max
            else:
                oposite_color = 'w'
                color_optimum = min
            root_node = Node('', MoveMockup(), 0, oposite_color)
            root_node.subnodes = [ Node(root_node.path, z, root_node.depth_level + 1, by_color) for z in game_state ]
            expansion_scores = []
            for sub_node in root_node.subnodes:
                sub_node_score = self.evaluate(sub_node, cutoff_depth)
                expansion_scores.append(sub_node_score)
                # print('node  count after move', sub_node.move, ':', nodecount)
                # print('root_node KB size', asizeof.asizeof(root_node)//1024)
                # print('game      KB size', asizeof.asizeof(self.game)//1024)
                # print('score_cache KB sz', asizeof.asizeof(self.score_cache)//1024)
            optimum = color_optimum(expansion_scores, key=lambda x: x.value)

            print('root node KB sz', asizeof.asizeof(root_node)//1024)
            return optimum

    def evaluate(self, node, cutoff_depth, upper_level_optimum=None):  # cutoff_depth absolute count of (semi-)turns
        # print('evaluate with arguments:', node, cutoff_depth, upper_level_optimum.value)
        if node.score != None:
            return node.score

        if node.depth_level == cutoff_depth:
            node.score = Score(self.score_node(node), node.path)
            # print('cutoff node:::', node.move.notation)
            # print('cutoff node    ', asizeof.asizeof(node))
            # print('cutoff move    ', asizeof.asizeof(node.move))
            # print('cutoff move piece    ', asizeof.asizeof(node.move.piece))
            # print('cutoff move origin   ', asizeof.asizeof(node.move.origin))
            # print('cutoff move type     ', asizeof.asizeof(node.move.type_))
            # print('cutoff move destin   ', asizeof.asizeof(node.move.destination))
            # print('cutoff move notati   ', asizeof.asizeof(node.move.notation))
            # print('cutoff move promo2   ', asizeof.asizeof(node.move.promote_to))
            # print('cutoff move taken    ', asizeof.asizeof(node.move.taken))
            # print('cutoff move cast_r   ', asizeof.asizeof(node.move.catsling_rook))

            # print('cutoff path    ', asizeof.asizeof(node.path))
            # print('cutoff depth   ', asizeof.asizeof(node.depth_level))
            # print('cutoff color   ', asizeof.asizeof(node.color))
            # print('cutoff optimum ', asizeof.asizeof(node.optimum))
            # print('cutoff len subs', len(node.subnodes))
            # print('cutoff subnodes', asizeof.asizeof(node.subnodes))
            # print('cutoff score   ', asizeof.asizeof(node.score))
            # print()
            return node.score
        else:
            # PLACE GAME IN THE RELEVANT NODE
            if node.move: # false in the case of mockup Node
                undo = self.game.board.execute_move(node.move)
                if self.game.turnning_player == self.game.whites_player:
                    self.game.turnning_player = self.game.blacks_player
                else:
                    self.game.turnning_player = self.game.whites_player
                self.game.history.append(node.move)
                self.game.backtrack.append(''.join(self.game.board.hashstate))

            if len(node.subnodes) == 0:
                self.expand_node(node)

            local_optimum = None
            expansion_scores = []
            if len(node.subnodes):
                for sub_node in node.subnodes:
                    sub_node_score = self.evaluate(sub_node, cutoff_depth, local_optimum)
                    expansion_scores.append(sub_node_score)
                    local_optimum = node.optimum(expansion_scores, key=lambda x: x.value)
                    # prune condition is: obtain local optimum that is more optimal than the upper_level_optimum
                    if upper_level_optimum and \
                                    local_optimum != None and \
                                    upper_level_optimum.value != local_optimum.value and \
                                    node.optimum(upper_level_optimum.value, local_optimum.value) == local_optimum.value:
                        break

            # push to chess-tree cache
            node.score = local_optimum

            # print(' .'*node.depth_level, str(node.move).ljust(6), ':', local_optimum, '      ', self.game.history)

            # RESTORE GAME TO PREDECESOR NODE
            if node.move:
                self.game.board.undo_actions(undo)
                if self.game.turnning_player == self.game.whites_player:
                    self.game.turnning_player = self.game.blacks_player
                else:
                    self.game.turnning_player = self.game.whites_player
                self.game.history.pop()
                self.game.backtrack.pop()

            return local_optimum

# class NodeMockup:

#     def __init__(self, not_starting_color='b'):
#         self.color = not_starting_color
#         self.move_chain = []

#     def remove_invalid_move_node(self, item):
#         pass

class MoveMockup:

    def __init__(self):
        self.notation = ''

# import pickle
from pympler import asizeof
import cProfile
from game import Game

nodecount = 0


# setup
# test_game = Game()
position = {'e2':'  ','c8':'  ','e1':'  ','b6':'  ','e8':'bk','e7':'  ','g5':'  ','b1':'  ','a2':'  ','g6':'  ','e6':'  ','f6':'  ','h4':'  ','h7':'bp','g1':'wk','a5':'wp','b2':'  ','d3':'wp','c1':'  ','e3':'  ','c4':'  ','a6':'bp','a4':'  ','d8':'  ','f3':'wp','a8':'br','d2':'  ','c6':'  ','c7':'bp','g8':'  ','d1':'wq','f2':'wp','f1':'wr','g3':'  ','g2':'  ','b8':'  ','c2':'wp','f8':'  ','b4':'bq','b7':'bp','f5':'  ','f4':'  ','d4':'bp','h3':'wp','a3':'  ','c3':'  ','b3':'  ','d7':'  ','b5':'  ','e4':'wn','h6':'  ','d5':'  ','h2':'  ','h8':'br','a1':'wr','h1':'  ','g4':'  ','g7':'bp','h5':'  ','c5':'  ','a7':'bb','f7':'bp','e5':'  ','d6':'  '}
test_game = Game(board_position=position)
test_ai = AI(4, test_game) # this cutoff value is not used, but the one passed in the evaluate method


# cProfile.run('test = test_ai.evaluate_position("w", 3)')
test = test_ai.evaluate_position("w", 3)
print(test_game.board)
print('optimal move with score', test.value, 'and move path:', test.optimal_cutoff_path)

