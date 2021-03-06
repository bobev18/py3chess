# from pympler import asizeof
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
    def __init__(self, path, depth_level, color, move):
        self.move = move
        self.path = path + '|' + move.notation
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
            print('mate', game_state, 'turning pl', self.game.turnning_player.color)
            print(board)
            return 1000
        elif game_state == 'stalemate':
            print('stalemate', game_state, 'turning pl', self.game.turnning_player.color)
            print(board)
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
        undo = self.game.board.execute_move(node.move)
        if self.game.turnning_player == self.game.whites_player:
            self.game.turnning_player = self.game.blacks_player
        else:
            self.game.turnning_player = self.game.whites_player
        self.game.record_history(node.move)
        self.game.whites_player.is_in_check = self.game.board.white_checked
        self.game.blacks_player.is_in_check = self.game.board.black_checked
        game_state = self.game.determine_game_state()
        try:
            score = self.score_cache[self.game.board.hashstate]
        except KeyError:
            score = self.evaluator(game_state, self.game.board)
            self.score_cache[self.game.board.hashstate] = score

        if isinstance(game_state, list):
            node.subnodes = sorted([ Node(node.path, node.depth_level + 1, not node.color, z) for z in game_state ], key=lambda x: x.path)

        self.game.board.undo_move(undo)
        if self.game.turnning_player == self.game.whites_player:
            self.game.turnning_player = self.game.blacks_player
        else:
            self.game.turnning_player = self.game.whites_player
        self.game.history.pop()
        self.game.special_moves.pop()
        self.game.backtrack.pop()
        print('cutoffnode', node, node.move, score)
        return score

    def expand_node(self, node):
        # this method is called for nodes that are already executed onto the game object
        game_state = self.game.determine_game_state()   # returns 'mate', 'stalemate', or list of all valid expansions
        if isinstance(game_state, list):
            print(node, game_state)
            node.subnodes = sorted([ Node(node.path, node.depth_level + 1, not node.color, z) for z in game_state ], key=lambda x: x.path)
            return None
        else:
            print('NOT LIST', node, game_state, self.evaluator(game_state, None))
            # return self.evaluator(game_state, None)    #board is irrelevant because evaluator does not reference board when gamestate type is str
            return Score(self.evaluator(game_state, None), node.path)    #board is irrelevant because evaluator does not reference board when gamestate type is str

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
            root_node = Node('', 0, oposite_color, MoveMockup())
            # game_state.sort(key = lambda x: x.notation)
            game_state = [ z for z in game_state if z.notation == 'Qa3' ]
            first_move = game_state.pop()
            first_node = Node(root_node.path, root_node.depth_level + 1, by_color=='w', first_move)
            optimum = self.evaluate(first_node, cutoff_depth)
            optimal_node = first_node
            print('first node', first_node.move.notation, 'opt score', optimum.value, optimum.optimal_cutoff_path)
            for sub_move in game_state:
                sub_node = Node(root_node.path, root_node.depth_level + 1, by_color=='w', sub_move)
                sub_node_score = self.evaluate(sub_node, cutoff_depth)
                if color_optimum(optimum.value, sub_node_score.value) != optimum.value:
                    optimum = sub_node_score
                    optimal_node = sub_node
                    print('new optimum', optimum.value, optimum.optimal_cutoff_path)

            root_node.subnodes = [optimal_node]
            return optimum

    def evaluate(self, node, cutoff_depth, upper_level_optimum=None):  # cutoff_depth absolute count of (semi-)turns
        # print('evaluate move', node.move)
        # print('evaluate with arguments:', node, cutoff_depth)
        # if upper_level_optimum: print('upper_level_optimum.value', upper_level_optimum.value)
        if node.depth_level == cutoff_depth:
            # print('cutoff node:::', node.move.notation, node.path, )#node.score.value)
            return Score(self.score_node(node), node.path)
        else:
            # PLACE GAME IN THE RELEVANT NODE
            undo = self.game.board.execute_move(node.move)
            if self.game.turnning_player == self.game.whites_player:
                self.game.turnning_player = self.game.blacks_player
            else:
                self.game.turnning_player = self.game.whites_player
            self.game.whites_player.is_in_check = self.game.board.white_checked
            self.game.blacks_player.is_in_check = self.game.board.black_checked
            self.game.record_history(node.move)

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
            self.game.board.undo_move(undo)
            if self.game.turnning_player == self.game.whites_player:
                self.game.turnning_player = self.game.blacks_player
            else:
                self.game.turnning_player = self.game.whites_player
            self.game.history.pop()
            self.game.special_moves.pop()
            self.game.backtrack.pop()

            return local_optimum


# sacrifice pos
position = {
    'a8':'  ','b8':'  ','c8':'bk','d8':'br','e8':'  ','f8':'  ','g8':'  ','h8':'br',
    'a7':'bp','b7':'bp','c7':'  ','d7':'bq','e7':'  ','f7':'bp','g7':'bp','h7':'bp',
    'a6':'  ','b6':'  ','c6':'  ','d6':'  ','e6':'  ','f6':'bn','g6':'  ','h6':'  ',
    'a5':'  ','b5':'wn','c5':'bb','d5':'  ','e5':'  ','f5':'  ','g5':'  ','h5':'  ',
    'a4':'  ','b4':'  ','c4':'wp','d4':'bp','e4':'  ','f4':'wb','g4':'  ','h4':'  ',
    'a3':'  ','b3':'  ','c3':'  ','d3':'  ','e3':'  ','f3':'  ','g3':'  ','h3':'wq',
    'a2':'wp','b2':'  ','c2':'  ','d2':'  ','e2':'  ','f2':'wp','g2':'wp','h2':'wp',
    'a1':'  ','b1':'wr','c1':'  ','d1':'  ','e1':'  ','f1':'wr','g1':'wk','h1':'  '
}
# |  |  |bk|br|  |  |  |br|
# |bb|bp|  |bq|  |bp|bp|bp|
# |  |  |  |  |  |bn|  |  |
# |  |wn|bb|  |  |  |  |  |
# |  |  |wp|bp|  |wb|  |  |
# |  |  |  |  |  |  |  |wq|
# |wp|  |  |  |  |wp|wp|wp|
# |  |wr|  |  |  |wr|wk|  |






# position = {'e2':'  ','c8':'  ','e1':'  ','b6':'  ','e8':'bk','e7':'  ','g5':'  ','b1':'  ','a2':'  ','g6':'  ','e6':'  ','f6':'  ','h4':'  ','h7':'bp','g1':'wk','a5':'wp','b2':'  ','d3':'wp','c1':'  ','e3':'  ','c4':'  ','a6':'bp','a4':'  ','d8':'  ','f3':'wp','a8':'br','d2':'  ','c6':'  ','c7':'bp','g8':'  ','d1':'wq','f2':'wp','f1':'wr','g3':'  ','g2':'  ','b8':'  ','c2':'wp','f8':'  ','b4':'bq','b7':'bp','f5':'  ','f4':'  ','d4':'bp','h3':'wp','a3':'  ','c3':'  ','b3':'  ','d7':'  ','b5':'  ','e4':'wn','h6':'  ','d5':'  ','h2':'  ','h8':'br','a1':'wr','h1':'  ','g4':'  ','g7':'bp','h5':'  ','c5':'  ','a7':'bb','f7':'bp','e5':'  ','d6':'  '}
# |br|  |  |  |bk|  |  |br|
# |bb|bp|bp|  |  |bp|bp|bp|
# |bp|  |  |  |  |  |  |  |
# |wp|  |  |  |  |  |  |  |
# |  |bq|  |bp|wn|  |  |  |
# |  |  |  |wp|  |wp|  |wp|
# |  |  |wp|  |  |wp|  |  |
# |wr|  |  |wq|  |wr|wk|  |
# b_loose_q_position = {'e2':'  ','c8':'  ','e1':'  ','b6':'  ','e8':'bk','e7':'  ','g5':'  ','b1':'wr','a2':'  ','g6':'  ','e6':'  ','f6':'  ','h4':'  ','h7':'bp','g1':'wk','a5':'wp','b2':'  ','d3':'wp','c1':'  ','e3':'  ','c4':'  ','a6':'bp','a4':'  ','d8':'  ','f3':'wp','a8':'br','d2':'  ','c6':'  ','c7':'bp','g8':'  ','d1':'wq','f2':'wp','f1':'wr','g3':'  ','g2':'  ','b8':'  ','c2':'wp','f8':'  ','b4':'bq','b7':'bp','f5':'  ','f4':'  ','d4':'bp','h3':'wp','a3':'  ','c3':'  ','b3':'  ','d7':'  ','b5':'  ','e4':'wn','h6':'  ','d5':'  ','h2':'  ','h8':'br','a1':'  ','h1':'  ','g4':'  ','g7':'bp','h5':'  ','c5':'  ','a7':'bb','f7':'bp','e5':'  ','d6':'  '}
# test_game = Game()
test_game = Game(board_position=position)
test_ai = AI(3, test_game) # this cutoff value is not used, but the one passed in the evaluate method

# test = test_ai.evaluate_position("w", 3)
cProfile.run('test = test_ai.evaluate_position("w", 4)')
print(test_game.board)
print('optimal move with score', test.value, 'and move path:', test.optimal_cutoff_path)


