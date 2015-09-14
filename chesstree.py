# class Game:
def validate_n_score_move(self, move, evaluator):
    if self.validate_against_history(move): # and move in self.board.naive_moves(move.piece): <--- we generated them based on naive move
        undo = self.board.execute_move(move)
        if undo:
            # print(self.board)
            hash_ = self.board.hashit()
            try:
                score = self.score_cache[hash_]
            except KeyError:
                score = evaluator(self.board)
                self.score_cache[hash_] = score
            self.board.undo_actions(undo) #    <----------------- should not be needed, but is, because we need to return to the previous board state before expanding new node @ cutoff level
            # print('vlidation & score', undo, score, )
            return hash_, score, undo
    return None, None, None



class Node:

    def __init__(self, predecessor, move, depth_level, color, *other_arguments):
        self.predecessor = predecessor
        # print(move)
        # print('predecessor', predecessor)
        # print('predecessor type', type(predecessor))
        # print('predecessor chain', predecessor.move_chain)
        self.move_chain = predecessor.move_chain.copy()
        self.move_chain.append(move)
        self.move = move
        # self.notation = notation  -- contained in the move
        self.depth_level = depth_level
        self.color = color
        if color == 'w':
            self.optimum = max
        else:
            self.optimum = min

        # these will gain value only if node is evaluated
        # self.hash = None
        self.naive_expansions = []
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
        # print('cutoff evaluation of move', self.move, ' at level', self.depth_level)
        # test = game.validate_n_score_move(self.move, evaluator)
        hash_, score, undo = game.validate_n_score_move(self.move, evaluator)
        # print('game.validate_n_score_move results: ', len(hash_), score, undo)
        if undo:
            self.scores[self.depth_level] = score
            self.hash = game.board.hashit()
            # print('cutoff score:', score)
            return score
        else:
            self.predecessor.remove_invalid_move_node(self)
            print('move ', self.move, ' is invalid')
            return None

    # # def optimum(self, scores):
    #     if self.color

    def remove_invalid_move_node(self, subnode):
        self.subnodes.remove(subnode)

# class ChessTree:
#     # should be possible to construct it from given position onwards
#     # provides methods for expansion

#     def __init__(self, *root_node_data):
#         self.game = # definitely needs a game
#         self.root = Node(*root_node_data)



class AI:

    def __init__(self, cutoff, game):
        self.game = game
        self.cutoff = cutoff
        # when starting the evaluate from outside use evaluate(node, node.depth_level + cutoff)

    def evaluator(self, board):
        return 3*len(board.white) - 3*len(board.black) + int(board.black_checked) - int(board.black_checked)

    def evaluate(self, node, cutoff_depth, upper_level_optimum=None):  ## cutoff_depth absolute count of (semi-)turns
        try:
            return node.scores[cutoff_depth]       # this could be possible if oponent makes "undo"
        except KeyError:
            pass

        if node.depth_level == cutoff_depth:
            # needs only to selfevaluate:
            #   execute the move && validate
            #   read cache or generate position score based on ai heuristic
            #   add score to cache if needed
            #   add level:selfscore in node.scores
            return node.selfevaluate(self.game, self.evaluator)
            # valid_move = node.selfevaluate(game, evaluator)
            # if valid_move:
            #     result = valid_move



            #     return node
        else:
            if node.move:
                undo = self.game.board.execute_move(node.move)
                self.game.history.append(node.move)
                # print(self.game.board)
            if not len(node.subnodes):
                node.expand(self.game.board)

            # /\ problem is above - new subnode generation is based of a gameboard that does not have move executions

            expansion_evaluations = {}
            naive_subnodes = node.subnodes.copy()
            local_optimum = None
            for sub_node in node.subnodes:
                # print('considering subnode at level', sub_node.depth_level, sub_node.move)
                sub_node_evaluation = self.evaluate(sub_node, cutoff_depth, local_optimum)
                print(sub_node.move, 'sneval', sub_node_evaluation, 'chain', sub_node.move_chain, '                 local_optimum', local_optimum)
                # if sub_node in node.subnodes:    # because evaluation process may invalidate thus delete the node from predecessor
                if sub_node_evaluation != None:    # because evaluation process may invalidate thus delete the node from predecessor
                    expansion_evaluations[sub_node.move.notation] = sub_node_evaluation
                    local_optimum = node.optimum(expansion_evaluations.values())

                # prune
                # prune depends on knowledge of the optimal score for the upper level!
                # condition is: obtain local optimum that is more optimal than the upper_level_optimum
                if upper_level_optimum and \
                                local_optimum != None and \
                                upper_level_optimum != local_optimum and \
                                node.optimum([upper_level_optimum, local_optimum]) == local_optimum:
                    print('prunning')
                    break

            node.scores[cutoff_depth] = local_optimum
            # if node.depth_level == 2:
            print(' .'*node.depth_level, str(node.move).ljust(6), ':', local_optimum, '      ', self.game.history)
            if node.move:
                try:
                    self.game.board.undo_actions(undo)
                    self.game.history.pop()
                except TypeError:
                    print('failed to undo move', node.move, 'with actions', undo)

            return local_optimum
            # # should return the optimum, and the move that achieves it
            # optimal_next_move = [ k for k,v in expansion_evaluations.items() if v == local_optimum ][0]
            # new_move_chain = move_chain.copy()
            # new_move_chain.append(optimal_next_move)
            # print('move', node.move, 'optimal next move', optimal_next_move, 'optimal score', local_optimum,'old_chain', move_chain, 'extended optimal chain', new_move_chain)
            # return local_optimum, new_move_chain





from game import Game
# from move import Move

Game.validate_n_score_move = validate_n_score_move
test_game = Game()
test_ai = AI(5, test_game)
class NodeMockup:

    def __init__(self, not_starting_color='b'):
        self.color = not_starting_color
        self.move_chain = []
        # self.scores = {}
        # self.level = 0
        # self.subnodes = []

    def remove_invalid_move_node(self, item):
        pass
# init_node = Node(NodeMockup(), None, 0, 'b') # predecessor, move, depth_level, color, *other_arguments):
# test = test_ai.evaluate(init_node, 3)
# print('score for a move that results in the initial game position', test)
# e4_node = Node(NodeMockup, Move(test_game.board.state['e2'], 'm2', 'e4', 'e4'), 1, 'w') #piece, type_, destination, notation, extra = None):

e2moves = test_game.valid_moves_of_piece_at('e2')
e4move = [z for z in e2moves if z.notation == 'e4'][0]
e4_node = Node(NodeMockup('w'), e4move, 1, 'b') #piece, type_, destination, notation, extra = None):
test = test_ai.evaluate(e4_node, 4)
print('score for opening e4', test)






