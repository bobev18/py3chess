
# def validate_n_score_move(self, move, evaluator):
#     if self.validate_against_history(move):
#         undo = self.board.execute_move(move)
#         if undo:
#             hash_ = ''.join(self.board.hashstate)
#             try:
#                 score = self.score_cache[hash_]
#             except KeyError:
#                 score = evaluator(self.board)
#                 self.score_cache[hash_] = score
#             self.board.undo_actions(undo)
#             return score
#     return None

def score_node(self, node, evaluator):
    # we know it's valid, because it would not be a node if it isn't
    undo = self.board.execute_move(node.move) # this is the move @ cutoff level
    game_state = self.determine_game_state() # returns 'mate', 'stalemate', or list of all valid expansions
    #                                       this executes moves at cutoff+1 level
    hash_ = hash(self.board.state)
    try:
        score = self.score_cache[hash_]
    except KeyError:
        score = evaluator(game_state, self.board)
        self.score_cache[hash_] = score
    
    if isinstance(game_state, list): # create new nodes
        node.subnodes = [  Node(node, z, node.depth_level + 1, node.predecessor.color) for z in game_state ]

    self.board.undo_actions(undo)
    return score

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

        # these will gain value only if node is evaluated
        self.subnodes = []
        self.scores = {}

    def __repr__(self):
        return str([self.move, self.move_chain])

    # def expand(self, board):
    #     # generates the child nodes by naive expansion
    #     self.naive_expansions = []
    #     for piece in board.pieces_of_color(self.color):
    #         self.naive_expansions.extend(board.naive_moves(piece))
    #     self.subnodes = [ Node(self, z, self.depth_level + 1, self.predecessor.color) for z in self.naive_expansions ]

    def selfevaluate(self, game, evaluator):
        score = game.score_node(self, evaluator)
        self.scores[self.depth_level] = score
        return score

    # def remove_invalid_move_node(self, subnode):
    #     self.subnodes.remove(subnode)

# class ChessTree:
#     # should be possible to construct it from given position onwards
#     # provides methods for expansion

#     def __init__(self, *root_node_data):
#         self.game = # definitely needs a game
#         self.root = Node(*root_node_data)

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

    def evaluator(self, game_state, board):
        if game_state == 'mate':
            return 1000
        elif game_state == 'stalemate':
            return 500*self.draw_desire
        else:
            # insert something with len(game_state) to consider number of moves available for the oponent
            return 3*len(board.white) - 3*len(board.black) + int(board.black_checked) - int(board.black_checked)

    def evaluate_position(self, by_color, cutoff_depth):
        game_state = self.game.determine_game_state()
        print('gamestate', game_state)
        if isinstance(game_state, str):
            return evaluator(game_state, self.game.board)
        else:
            if by_color == 'w':
                oposite_color = 'b'
            else:
                oposite_color = 'w'
            root_node = Node(NodeMockup(), None, 0, oposite_color)
            root_node.subnodes = [ Node(root_node, z, root_node.depth_level + 1, root_node.predecessor.color) for z in game_state ]
            print('root_node subnodes', root_node.subnodes)
            return self.evaluate(root_node, cutoff_depth)

    def evaluate(self, node, cutoff_depth, upper_level_optimum=None):  # cutoff_depth absolute count of (semi-)turns
        try: # read from chess-tree cache
            print('read from cache', node.scores[cutoff_depth])
            return node.scores[cutoff_depth]       # this could be possible if oponent makes "undo"
        except KeyError:
            pass

        if node.depth_level == cutoff_depth:
            print('cutoff', node, 'score ...')
            return Score(node.selfevaluate(self.game, self.evaluator), node)
        else:
            if node.move: # false in the case of mockup Node
                print('node', node.move)
                undo = self.game.board.execute_move(node.move)
                self.game.history.append(node.move)

            # if not len(node.subnodes):
            #     node.expand(self.game.board)

            expansion_scores = []
            # subnodes = node.subnodes.copy()
            local_optimum = None
            for sub_node in node.subnodes:
                # sub_node = subnodes.pop() # replace _subnodes.pop() with method that prioritizes which moves to explore first of the moves i.e those that capture, or involve check
                sub_node_score = self.evaluate(sub_node, cutoff_depth, local_optimum)
                print('sub_score for', sub_node,'is', sub_node_score )
                # if sub_node_score.value != None:    # because value can be 0, and 0 evaluates to False
                # there are no invalid/naive nodes
                expansion_scores.append(sub_node_score)
                print('local expansion scores', expansion_scores)
                local_optimum = node.optimum(expansion_scores, key=lambda x: x.value)
                # else:
                #     node.subnodes.remove(sub_node)

                # prune
                # prune depends on knowledge of the optimal score for the upper level!
                # condition is: obtain local optimum that is more optimal than the upper_level_optimum
                if upper_level_optimum and \
                                local_optimum != None and \
                                upper_level_optimum.value != local_optimum.value and \
                                node.optimum(upper_level_optimum.value, local_optimum.value) == local_optimum.value:
                    # print(sub_node.move, 'prunning', [ z.move.notation for z in naive_subnodes])
                    break

            # push to chess-tree cache
            node.scores[cutoff_depth] = local_optimum

            # print(' .'*node.depth_level, str(node.move).ljust(6), ':', local_optimum, '      ', self.game.history)
            if node.move:
                self.game.board.undo_actions(undo)
                self.game.history.pop()

            return local_optimum

class NodeMockup:

    def __init__(self, not_starting_color='b'):
        self.color = not_starting_color
        self.move_chain = []

    def remove_invalid_move_node(self, item):
        pass

from game import Game
from move import Move
Game.score_node = score_node

MOCKUP_POSITION = {
    'a8':'br', 'b8':'  ', 'c8':'bb', 'd8':'bq', 'e8':'bk', 'f8':'bb', 'g8':'bn', 'h8':'br',
    'a7':'bp', 'b7':'bp', 'c7':'bp', 'd7':'bp', 'e7':'bp', 'f7':'bp', 'g7':'bp', 'h7':'bp',
    'a6':'  ', 'b6':'  ', 'c6':'bn', 'd6':'  ', 'e6':'  ', 'f6':'  ', 'g6':'  ', 'h6':'  ',
    'a5':'  ', 'b5':'  ', 'c5':'  ', 'd5':'  ', 'e5':'  ', 'f5':'  ', 'g5':'  ', 'h5':'  ',
    'a4':'  ', 'b4':'  ', 'c4':'  ', 'd4':'  ', 'e4':'  ', 'f4':'  ', 'g4':'  ', 'h4':'  ',
    'a3':'  ', 'b3':'  ', 'c3':'  ', 'd3':'  ', 'e3':'  ', 'f3':'  ', 'g3':'  ', 'h3':'  ',
    'a2':'wp', 'b2':'wp', 'c2':'wp', 'd2':'wp', 'e2':'wp', 'f2':'wp', 'g2':'wp', 'h2':'wp',
    'a1':'wr', 'b1':'wn', 'c1':'wb', 'd1':'wq', 'e1':'wk', 'f1':'wb', 'g1':'wn', 'h1':'wr',
}

# setup
test_game = Game(board_position=MOCKUP_POSITION)
test_ai = AI(5, test_game) # this cutoff value is not used, but the one passed in the evaluate method

# # prep move
# e2moves = test_game.valid_moves_of_piece_at('e2')
# e4move = [z for z in e2moves if z.notation == 'e4'][0]
# # evaluate specific move
# e4_node = Node(NodeMockup('w'), e4move, 1, 'b') #piece, type_, destination, notation, extra = None):
# test = test_ai.evaluate(e4_node, 4)
# print('score for opening e4', test.value)

# evaluate position
###### to evaluate position, we need the move leadin to it (inbound move).
###### If we lack such move, we can generate all valid moves available in the given the position and use them to 
###### populate mockup_node.subnodes

# # MOVE __init__(self, piece, type_, destination, notation, extra = None):
# mockup_inbound_move = Move(test_game.board.state['c6'], 'km', 'b8', 'Nb8')
# # NODE __init__(self, predecessor, move, depth_level, color, *other_arguments):
# mockup_node = Node(NodeMockup(), mockup_inbound_move, 0, 'w') # predecessor, move, depth_level, color, *other_arguments):
# mockup_node 
# # import cProfile
# # cProfile.run('test = test_ai.evaluate(mockup_node, 5)')
# test = test_ai.evaluate(mockup_node, 5)
test = test_ai.evaluate_position('w', 5)

print('optimal move', test.optimal_cutoff_node.move_chain[0], 'with score', test.value, 'and move path:', test.optimal_cutoff_node.move_chain)
