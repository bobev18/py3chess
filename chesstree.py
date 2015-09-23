from pympler import asizeof
import cProfile
from game import Game


class MoveMockup:
    def __init__(self):
        self.notation = ''


class Score:
    def __init__(self, value, optimal_cutoff_path):
        self.value = value
        self.optimal_cutoff_path = optimal_cutoff_path


class Node:
    def __init__(self, notation, path, depth_level, color, move_actions=[], undo_actions=[]):
        self.move_actions = move_actions
        self.undo_actions = undo_actions
        self.notation = notation
        self.path = path + '|' + notation
        self.depth_level = depth_level
        self.subnodes = []
        self.color = color
        if color:
            self.optimum = min
        else:
            self.optimum = max

    def __repr__(self):
        return str([self.move.notation, self.color, self.depth_level, self.path[1:]])


class AI:
    def __init__(self, cutoff, game):
        self.game = game
        self.cutoff = cutoff
        # when starting the evaluate from outside use evaluate(node, node.depth_level + cutoff)
        self.draw_desire = -1 # can be in range [-1..1] where -1 means doesn't want draw, 1 means wants draw, and 0 = indifferent
        self.score_cache = {}

    def evaluator(self, game_state, board):
        if game_state == 'mate':
            return 1000
        elif game_state == 'stalemate':
            return 500*self.draw_desire
        else:
            def pieceset_value(pieceset):
                queens = len([ z for z in pieceset if z.type_ == 'q'])*10
                rooks = len([ z for z in pieceset if z.type_ == 'r'])*5
                bishkni = len([ z for z in pieceset if z.type_ == 'b' or z.type_ == 'n'])*3
                pawns = len([ z for z in pieceset if z.type_ == 'p'])
                return queens + rooks + bishkni + pawns

            def board_position_value(pieceset):
                inner_center = len([ z for z in pieceset if z.location in ['d5', 'e5', 'd4', 'e4']])
                outer_center = len([ z for z in pieceset if z.location in ['c6', 'd6', 'e6', 'f6', 'c5', 'f5', 'c4', 'f4', 'c3', 'd3', 'e3', 'f3']])
                return inner_center*2 + outer_center*1

            # insert something with len(game_state) to consider number of moves available for the opponent
            return 9*pieceset_value(board.white) - 9*pieceset_value(board.black) + 3*int(board.black_checked) - 3*int(board.black_checked) + board_position_value(board.white) - board_position_value(board.black)

    def score_node(self, node):
        wchecked, bchecked = self.game.board.execute_flat(node.move_actions)
        node.undo_actions[-2] = wchecked
        node.undo_actions[-1] = bchecked
        self.game.board.update_incheck(node.color*'w')
        game_state = self.game.determine_game_state()
        try:
            score = self.score_cache[self.game.board.hashstate]
        except KeyError:
            score = self.evaluator(game_state, self.game.board)
            self.score_cache[self.game.board.hashstate] = score

        if isinstance(game_state, list):
            node.subnodes = [ Node(z.notation, node.path, node.depth_level + 1, not node.color, *z.flat_actions()) for z in game_state ]

        self.game.board.process_flat_actions(node.undo_actions)
        return score

    def expand_node(self, node):
        # this method is called for nodes that are already executed onto the game object
        game_state = self.game.determine_game_state()   # returns 'mate', 'stalemate', or list of all valid expansions
        if isinstance(game_state, list):
            node.subnodes = [ Node(z.notation, node.path, node.depth_level + 1, not node.color, *z.flat_actions()) for z in game_state ]
            return None
        else:
            return self.evaluator(game_state, None)    #board is irrelevant because evaluator does not reference board when gamestate type is str

    def evaluate_position(self, by_color, cutoff_depth):
        game_state = self.game.determine_game_state()
        if isinstance(game_state, str):
            return evaluator(game_state, self.game.board)
        else:
            if by_color == 'w':
                oposite_color = 'b'
                color_optimum = max
            else:
                oposite_color = 'w'
                color_optimum = min
            root_node = Node('', '', 0, oposite_color)
            first_move = game_state.pop()
            first_node = Node(first_move.notation, root_node.path, root_node.depth_level + 1, by_color=='w', *first_move.flat_actions())
            optimum = self.evaluate(first_node, cutoff_depth)
            optimal_node = first_node
            print('first node', first_node.notation, 'opt score', optimum.value, optimum.optimal_cutoff_path)
            for sub_move in game_state:
                sub_node = Node(sub_move.notation, root_node.path, root_node.depth_level + 1, by_color=='w', *sub_move.flat_actions())
                sub_node_score = self.evaluate(sub_node, cutoff_depth)
                if color_optimum(optimum.value, sub_node_score.value) != optimum.value:
                    optimum = sub_node_score
                    optimal_node = sub_node
                    print('new optimum', optimum.value, optimum.optimal_cutoff_path)

                # print('optimal_node KB size', asizeof.asizeof(optimal_node)//1024)
                # print('sub_node KB size', asizeof.asizeof(sub_node)//1024)
                # print('game      KB size', asizeof.asizeof(self.game)//1024)
                # print('score_cache KB sz', asizeof.asizeof(self.score_cache)//1024)
            root_node.subnodes = [optimal_node]

            print('final root node size (KB)', asizeof.asizeof(root_node)//1024)
            return optimum

    def evaluate(self, node, cutoff_depth, upper_level_optimum=None):  # cutoff_depth absolute count of (semi-)turns
        # print('evaluate with arguments:', node, cutoff_depth, upper_level_optimum.value)
        if node.depth_level == cutoff_depth:
            # print('cutoff node:::', node.notation, node.path, node.score.value)
            # print('cutoff node    ', asizeof.asizeof(node))
            return Score(self.score_node(node), node.path)
        else:
            # PLACE GAME IN THE RELEVANT NODE
            print('move_actions', node.move_actions)
            wchecked, bchecked = self.game.board.execute_flat(node.move_actions)
            node.undo_actions[-2] = wchecked
            node.undo_actions[-1] = bchecked
            self.game.board.update_incheck(self.game.turnning_player.color)
            if self.game.turnning_player == self.game.whites_player:
                self.game.turnning_player = self.game.blacks_player
            else:
                self.game.turnning_player = self.game.whites_player
            self.game.record_flat_history(node.move_actions, node.notation)

            if len(node.subnodes) == 0:
                local_optimum = self.expand_node(node)   # returns score if mate or stalemate
            else:
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
                        # print('prune@', sub_node.notation, ': upper opt [', upper_level_optimum.value, upper_level_optimum.optimal_cutoff_path, ']; local opt', local_optimum.value)
                        # print('currnt node', node.notation, 'col', node.color, 'opt func', node.optimum.__name__)
                        # print('all cycle nodes', [ z.notation for z in node.subnodes ])
                        break

            # RESTORE GAME TO PREDECESOR NODE
            self.game.board.process_flat_actions(node.undo_actions)
            if self.game.turnning_player == self.game.whites_player:
                self.game.turnning_player = self.game.blacks_player
            else:
                self.game.turnning_player = self.game.whites_player
            self.game.special_moves.pop()
            self.game.backtrack.pop()

            return local_optimum





position = {'e2':'  ','c8':'  ','e1':'  ','b6':'  ','e8':'bk','e7':'  ','g5':'  ','b1':'  ','a2':'  ','g6':'  ','e6':'  ','f6':'  ','h4':'  ','h7':'bp','g1':'wk','a5':'wp','b2':'  ','d3':'wp','c1':'  ','e3':'  ','c4':'  ','a6':'bp','a4':'  ','d8':'  ','f3':'wp','a8':'br','d2':'  ','c6':'  ','c7':'bp','g8':'  ','d1':'wq','f2':'wp','f1':'wr','g3':'  ','g2':'  ','b8':'  ','c2':'wp','f8':'  ','b4':'bq','b7':'bp','f5':'  ','f4':'  ','d4':'bp','h3':'wp','a3':'  ','c3':'  ','b3':'  ','d7':'  ','b5':'  ','e4':'wn','h6':'  ','d5':'  ','h2':'  ','h8':'br','a1':'wr','h1':'  ','g4':'  ','g7':'bp','h5':'  ','c5':'  ','a7':'bb','f7':'bp','e5':'  ','d6':'  '}
# b_loose_q_position = {'e2':'  ','c8':'  ','e1':'  ','b6':'  ','e8':'bk','e7':'  ','g5':'  ','b1':'wr','a2':'  ','g6':'  ','e6':'  ','f6':'  ','h4':'  ','h7':'bp','g1':'wk','a5':'wp','b2':'  ','d3':'wp','c1':'  ','e3':'  ','c4':'  ','a6':'bp','a4':'  ','d8':'  ','f3':'wp','a8':'br','d2':'  ','c6':'  ','c7':'bp','g8':'  ','d1':'wq','f2':'wp','f1':'wr','g3':'  ','g2':'  ','b8':'  ','c2':'wp','f8':'  ','b4':'bq','b7':'bp','f5':'  ','f4':'  ','d4':'bp','h3':'wp','a3':'  ','c3':'  ','b3':'  ','d7':'  ','b5':'  ','e4':'wn','h6':'  ','d5':'  ','h2':'  ','h8':'br','a1':'  ','h1':'  ','g4':'  ','g7':'bp','h5':'  ','c5':'  ','a7':'bb','f7':'bp','e5':'  ','d6':'  '}
# test_game = Game()
test_game = Game(board_position=position)
test_ai = AI(4, test_game) # this cutoff value is not used, but the one passed in the evaluate method

test = test_ai.evaluate_position("w", 3)
# cProfile.run('test = test_ai.evaluate_position("w", 4)')
print(test_game.board)
print('optimal move with score', test.value, 'and move path:', test.optimal_cutoff_path)

