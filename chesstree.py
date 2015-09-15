
def validate_n_score_move(self, move, evaluator):
    if self.validate_against_history(move):
        undo = self.board.execute_move(move)
        if undo:
            hash_ = ''.join(self.board.hashstate)
            try:
                score = self.score_cache[hash_]
            except KeyError:
                score = evaluator(self.board)
                self.score_cache[hash_] = score
            self.board.undo_actions(undo)
            return score
    return None

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

    def expand(self, board):
        # generates the child nodes by naive expansion
        self.naive_expansions = []
        for piece in board.pieces_of_color(self.color):
            self.naive_expansions.extend(board.naive_moves(piece))
        self.subnodes = [ Node(self, z, self.depth_level + 1, self.predecessor.color) for z in self.naive_expansions ]

    def selfevaluate(self, game, evaluator):
        score = game.validate_n_score_move(self.move, evaluator)
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

    def evaluator(self, board):
        return 3*len(board.white) - 3*len(board.black) + int(board.black_checked) - int(board.black_checked)

    def evaluate(self, node, cutoff_depth, upper_level_optimum=None):  # cutoff_depth absolute count of (semi-)turns
        try: # read from chess-tree cache
            return node.scores[cutoff_depth]       # this could be possible if oponent makes "undo"
        except KeyError:
            pass

        if node.depth_level == cutoff_depth:
            return Score(node.selfevaluate(self.game, self.evaluator), node)
        else:
            if node.move: # false in the case of mockup Node
                undo = self.game.board.execute_move(node.move)
                self.game.history.append(node.move)

            if not len(node.subnodes):
                node.expand(self.game.board)

            expansion_scores = []
            subnodes = node.subnodes.copy()
            local_optimum = None
            while len(subnodes):
                sub_node = subnodes.pop() # replace _subnodes.pop() with method that prioritizes which moves to explore first of the moves i.e those that capture, or involve check
                sub_node_score = self.evaluate(sub_node, cutoff_depth, local_optimum)
                if sub_node_score.value != None:    # because value can be 0, and 0 evaluates to False
                    expansion_scores.append(sub_node_score)
                    local_optimum = node.optimum(expansion_scores, key=lambda x: x.value)
                else:
                    node.subnodes.remove(sub_node)

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
                try:
                    self.game.board.undo_actions(undo)
                    self.game.history.pop()
                except TypeError:
                    print('failed to undo move', node.move, 'with actions', undo)

            return local_optimum

class NodeMockup:

    def __init__(self, not_starting_color='b'):
        self.color = not_starting_color
        self.move_chain = []

    def remove_invalid_move_node(self, item):
        pass

from game import Game
Game.validate_n_score_move = validate_n_score_move

# setup
test_game = Game()
test_ai = AI(5, test_game) # this cutoff value is not used, but the one passed in the evaluate method

# # prep move
# e2moves = test_game.valid_moves_of_piece_at('e2')
# e4move = [z for z in e2moves if z.notation == 'e4'][0]
# # evaluate specific move
# e4_node = Node(NodeMockup('w'), e4move, 1, 'b') #piece, type_, destination, notation, extra = None):
# test = test_ai.evaluate(e4_node, 4)
# print('score for opening e4', test.value)

# evaluate position
mockup_node = Node(NodeMockup(), None, 0, 'w') # predecessor, move, depth_level, color, *other_arguments):

import cProfile
cProfile.run('test = test_ai.evaluate(mockup_node, 4)')

print('optimal move', test.optimal_cutoff_node.move_chain[0], 'with score', test.value, 'and move path:', test.optimal_cutoff_node.move_chain)
