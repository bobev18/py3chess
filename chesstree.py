class Node:

    def __init__(self, predecessor, move, depth_level, color, *other_arguments):
        self.predecessor = predecessor
        self.move_chain = predecessor.move_chain.copy()
        self.move_chain.append(move)
        self.move = move
        self.depth_level = depth_level
        self.color = color
        if color == 'w':
            self.optimum = max
        else:
            self.optimum = min

        self.subnodes = []
        self.scores = {}

    def __repr__(self):
        return str([self.move, self.color, self.depth_level, self.move_chain[1:]])

class Score:

    def __init__(self, value, optimal_cutoff_node):
        self.value = value
        self.optimal_cutoff_node = optimal_cutoff_node

class AI:

    def __init__(self, cutoff, game):
        self.game = game
        self.cutoff = cutoff
        # when starting the evaluate from outside use evaluate(node, node.depth_level + cutoff)
        self.draw_desire = -1 # can be in range [-1..1] where -1 means doesnt want draw, 1 means wants draw, and 0 = indiferent
        self.score_cache = {}

    def expand_node(self, node):
        # this method is called for nodes that are already executed onto the game object
        game_state = self.game.determine_game_state() # returns 'mate', 'stalemate', or list of all valid expansions
        if isinstance(game_state, list): # create new nodes
            node.subnodes = [  Node(node, z, node.depth_level + 1, node.predecessor.color) for z in game_state ]

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
            node.subnodes = [ Node(node, z, node.depth_level + 1, node.predecessor.color) for z in game_state ]

        self.game.board.undo_actions(undo)
        return score

    def evaluator(self, game_state, board):
        if game_state == 'mate':
            return 1000
        elif game_state == 'stalemate':
            print(self.game.board)
            print ('whaaaat')
            raise Exception
            return 500*self.draw_desire
        else:
            # insert something with len(game_state) to consider number of moves available for the oponent
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
            root_node = Node(NodeMockup(), '', 0, oposite_color)
            root_node.subnodes = [ Node(root_node, z, root_node.depth_level + 1, by_color) for z in game_state ]
            expansion_scores = []
            for sub_node in root_node.subnodes:
                sub_node_score = self.evaluate(sub_node, cutoff_depth)
                expansion_scores.append(sub_node_score)
            optimum = color_optimum(expansion_scores, key=lambda x: x.value)
            return optimum

    def evaluate(self, node, cutoff_depth, upper_level_optimum=None):  # cutoff_depth absolute count of (semi-)turns
        # print('evaluate with arguments:', node, cutoff_depth, upper_level_optimum.value)
        try:
            return node.scores[cutoff_depth]
        except KeyError:
            pass

        if node.depth_level == cutoff_depth:
            score = Score(self.score_node(node), node)
            node.scores[node.depth_level] = score
            return score
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
            node.scores[cutoff_depth] = local_optimum

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

class NodeMockup:

    def __init__(self, not_starting_color='b'):
        self.color = not_starting_color
        self.move_chain = []

    def remove_invalid_move_node(self, item):
        pass

import cProfile
from game import Game

# setup
test_game = Game()
test_ai = AI(4, test_game) # this cutoff value is not used, but the one passed in the evaluate method

cProfile.run('test = test_ai.evaluate_position("w", 3)')

print('optimal move', test.optimal_cutoff_node.move_chain[1], 'with score', test.value, 'and move path:', test.optimal_cutoff_node.move_chain[1:])
