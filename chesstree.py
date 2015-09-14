# class Game:
def validate_n_score_move(self, move, evaluator):
    if self.validate_against_history(move): # and move in self.board.naive_moves(move.piece): <--- we generated them based on naive move
        undo = self.board.execute_move(move)
        if undo:
            print(self.board)
            hash_ = self.board.hashit()
            try:
                score = self.score_cache[hash_]
            except KeyError:
                score = evaluator(self.board)
                self.score_cache[hash_] = score
            # self.board.undo_actions(undo)     <----------------- should not be needed
            return hash_, score, undo
    return None, None



class Node:

    def __init__(self, predecessor, move, depth_level, color, *other_arguments):
        self.predecessor = predecessor
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

    def expand(self, board):
        # generates the child nodes by naive expansion
        self.naive_expansions = []
        for piece in board.pieces_of_color(self.color):
            self.naive_expansions.extend(board.naive_moves(piece))
        self.subnodes = [ Node(self, z, self.depth_level + 1, self.predecessor.color) for z in self.naive_expansions ]
        
    def selfevaluate(self, game, evaluator):
        test = game.validate_n_score_move(self.move, evaluator)
        hash_, score = game.validate_n_score_move(self.move, evaluator)
        if score:
            self.scores[self.depth_level] = score
            self.hash = game.board.hashit()
            return score
        else:
            self.predecessor.remove_invalid_move_node(self)
            return None

    # # def optimum(self, scores):
    #     if self.color

    def remove_invalid_move_node(self, subnode):
        self.subnodes.remove(subnode)

# class ChessTree:
#     # should be possible to construct it from given position onwards
#     # provides methods for expansion

#     def __init__(self, *root_node_data):
#         slef.game = # definitely needs a game
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
            if not len(node.subnodes):
                node.expand(self.game.board)

            /\ problem is above - new subnode generation is based of a gameboard that does not have move executions

            expansion_evaluations = []
            naive_subnodes = node.subnodes.copy()
            local_optimum = None
            for sub_node in node.subnodes:
                print(sub_node.move)
                sub_node_evaluation = self.evaluate(sub_node, cutoff_depth, local_optimum)
                if sub_node in node.subnodes:    # because evaluation process may invalidate thus delete the node from predecessor
                    expansion_evaluations.append(sub_node_evaluation)

                local_optimum = node.optimum(expansion_evaluations)
                # prune
                # prune depends on knowledge of the optimal score for the upper level!
                # condition is: obtain local optimum that is more optimal than the upper_level_optimum
                if upper_level_optimum and \
                                upper_level_optimum != local_optimum and \
                                node.optimum([upper_level_optimum, local_optimum]) == local_optimum:
                    break

            node.scores[cutoff_depth] = local_optimum
            return local_optimum





from game import Game

Game.validate_n_score_move = validate_n_score_move
test_game = Game()
test_ai = AI(5, test_game)
class NodeMockup:

    def __init__(self, not_starting_color='b'):
        self.color = not_starting_color
        # self.scores = {}
        # self.level = 0
        # self.subnodes = []

    def remove_invalid_move_node(self, item):
        pass
mockup_node = Node(NodeMockup(), None, 0, 'w') # predecessor, move, depth_level, color, *other_arguments):
test_ai.evaluate(mockup_node, 5)




