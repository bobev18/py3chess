from board import Board
from piece import Piece
from player import Player
from move import Move

INITIAL_POSITION = {
    'a8':'br', 'b8':'bn', 'c8':'bb', 'd8':'bq', 'e8':'bk', 'f8':'bb', 'g8':'bn', 'h8':'br',
    'a7':'bp', 'b7':'bp', 'c7':'bp', 'd7':'bp', 'e7':'bp', 'f7':'bp', 'g7':'bp', 'h7':'bp',
    'a6':'  ', 'b6':'  ', 'c6':'  ', 'd6':'  ', 'e6':'  ', 'f6':'  ', 'g6':'  ', 'h6':'  ',
    'a5':'  ', 'b5':'  ', 'c5':'  ', 'd5':'  ', 'e5':'  ', 'f5':'  ', 'g5':'  ', 'h5':'  ',
    'a4':'  ', 'b4':'  ', 'c4':'  ', 'd4':'  ', 'e4':'  ', 'f4':'  ', 'g4':'  ', 'h4':'  ',
    'a3':'  ', 'b3':'  ', 'c3':'  ', 'd3':'  ', 'e3':'  ', 'f3':'  ', 'g3':'  ', 'h3':'  ',
    'a2':'wp', 'b2':'wp', 'c2':'wp', 'd2':'wp', 'e2':'wp', 'f2':'wp', 'g2':'wp', 'h2':'wp',
    'a1':'wr', 'b1':'wn', 'c1':'wb', 'd1':'wq', 'e1':'wk', 'f1':'wb', 'g1':'wn', 'h1':'wr',
}

# DEBUG helper  ---------------------
def attribute_lister(object_, attributes):
    return [ getattr(object_, z) for z in attributes ]
MOVE_ATTRIBUTES = ['piece', 'origin', 'type_', 'destination', 'notation', 'promote_to', 'taken', 'catsling_rook',]
#  end of DEBUG helper -------------

class SimulationException(Exception):
    # to handle erroneous moves provided in simulation
    def __init__(self, *args):
        self.args = [a for a in args]

class Game():

    def __init__(self, whites_player_type='human', blacks_player_type='human', clock=60*60, board_position={}, logfile='d:/temp/chesslog.txt'):
        if board_position:
            self.board = Board(board_position)
        else:
            self.board = Board(INITIAL_POSITION)
        self.whites_player = Player(self, whites_player_type, 'w', clock)
        self.blacks_player = Player(self, blacks_player_type, 'b', clock)
        self.turnning_player = self.whites_player
        self.opposing_player = self.blacks_player
        self.turn_count = 1
        self.semi_turn_count = 0
        self.undo_stack = []
        # self.full_notation = '' # quite as the values in hist, but with the count and # + ? !
        self.history = []
        self.special_moves = [[False, False, False, False, '']]         # to check past Moves of King or Rooks or enpassant setup
        self.backtrack = []       # past positions - to check for repetition draw
        self.score_cache = {}
        self.move_cache = {}
        self.state = 'init'
        with open(logfile,'wt') as f:
            self.logfile = f

    def full_notation(self):
        result = ''
        count = 1
        history = self.history.copy()
        while len(history):
            white_move = history.pop(0)
            result += str(count).rjust(3) + '. ' + white_move.notation + '  '
            if len(history):
                black_move = history.pop(0)
                result += black_move.notation + '\n'
            count += 1

        return result

    def determine_game_state(self):
        # draw - no one could possibly mate
        if len(self.board.white) + len(self.board.black) <= 2:
            return 'stalemate'

        if len(self.board.white) + len(self.board.black) == 3:
            if len(self.board.white) > len(self.board.black):
                extra_piece = [ z.type_ for z in self.board.white if z.type_ != 'k'][0]
            else:
                extra_piece = [ z.type_ for z in self.board.black if z.type_ != 'k'][0]
            if extra_piece in ['n', 'b']:
                return 'stalemate'

        # reduced ability to move
        valid_moves = []
        turning_pieceset = self.board.pieces_of_color(self.turnning_player.color).copy()   # copy because `valid_moves_of_piece_at` may alter it
        for piece in turning_pieceset:
            piece_valid_moves = self.valid_moves_of_piece(piece)
            valid_moves.extend(piece_valid_moves)

        if len(valid_moves) == 0:
            if self.turnning_player.is_in_check:
                return 'mate'
            else:
                return 'stalemate'
        else:
            # repeated moves
            if len(self.backtrack) > 0 and self.backtrack.count(self.backtrack[-1]) >= 3:
                return 'stalemate'

        return valid_moves

    def record_history(self, move):
        history_dependant_move_state = [ self.special_moves[-1][0] or move.origin in ['a8', 'e8'],
                                         self.special_moves[-1][1] or move.origin in ['e8', 'h8'],
                                         self.special_moves[-1][2] or move.origin in ['a1', 'e1'],
                                         self.special_moves[-1][3] or move.origin in ['e1', 'h1'],
                                         int(move.type_ == 'm2')*move.destination[0]
                                       ]
        self.special_moves.append(history_dependant_move_state)
        self.history.append(move)
        self.backtrack.append(self.board.hashstate)

    def validate_special_moves(self, move):
        if move.type_ == 'c':
            if move.catsling_rook.location == 'a8':
                return not self.special_moves[-1][0]        # because the field being True indicates move is no longer valid
            elif move.catsling_rook.location == 'h8':
                return not self.special_moves[-1][1]
            elif move.catsling_rook.location == 'a1':
                return not self.special_moves[-1][2]
            elif move.catsling_rook.location == 'h1':
                return not self.special_moves[-1][3]
        if move.type_ == 'e':
             return self.special_moves[-1][4] == move.destination[0]

        return True

    def valid_moves_of_piece_at(self, location):
        # used only to ease construction of assertions in the unit tests
        return self.valid_moves_of_piece(self.board.state[location])

    def valid_moves_of_piece(self, piece):
        valid_moves = []
        # for move in self.board.naive_moves(piece):
        for pre_move in piece.naive_moves():
            # check for the move in cache
            move_key = (piece.color, piece.location) + pre_move
            try:
            # if move_key in self.move_cache.keys():
                move = self.move_cache[move_key]
            except KeyError:
            # else:
                move = Move(piece, *pre_move)
                self.move_cache[move_key] = move

            if self.validate_special_moves(move):
                if self.board.prevalidate_move(move):
                    valid_moves.append(move)

        return valid_moves

    def undo_last(self):
        # undo opponent move
        undo = self.undo_stack.pop()
        self.board.undo_move(undo)
        temp = self.history.pop()
        temp = self.special_moves.pop()
        self.backtrack.pop()
        # undo last own move
        undo = self.undo_stack.pop()
        self.board.undo_move(undo)
        temp = self.history.pop()
        temp = self.special_moves.pop()
        self.backtrack.pop()
        # repopulate the state, so that validation check passes
        self.state = self.determine_game_state()

    def start(self, verbose = True):
        self.state = self.determine_game_state()
        if verbose:
            self.turnning_player.comm_output(self.board)
            self.turnning_player.comm_output('state:', self.state)
            self.turnning_player.comm_output('-'*50)
        while isinstance(self.state, list): # == 'active':
            valid_input = False
            while not valid_input:
                decoded_move = self.turnning_player.prompt_input()
                if isinstance(decoded_move, str):  # in ['draw', 'forefit', 'quit', 'exit']:
                    valid_input = decoded_move
                else:
                    # print('mv, st, mv in st', decoded_move, self.state, decoded_move in self.state)
                    # fake_move = [ z for z in self.state if z.notation == decoded_move.notation][0]
                    # print(' '*10, decoded_move.piece, '?', fake_move.piece, '=', decoded_move.piece == fake_move.piece)
                    # print(' '*10, decoded_move.origin, '?', fake_move.origin, '=', decoded_move.origin == fake_move.origin)
                    # print(' '*10, decoded_move.type_[0], '?', fake_move.type_[0], '=', decoded_move.type_[0] == fake_move.type_[0])
                    # print(' '*10, decoded_move.destination, '?', fake_move.destination, '=', decoded_move.destination == fake_move.destination)
                    # print(' '*10, str(decoded_move.promote_to), '?', str(fake_move.promote_to), '=', str(decoded_move.promote_to) == str(fake_move.promote_to))
                    # print(' '*10, str(decoded_move.taken), '?', str(fake_move.taken), '=', str(decoded_move.taken) == str(fake_move.taken))
                    # print(' '*10, str(decoded_move.catsling_rook), '?', str(fake_move.catsling_rook), '=', str(decoded_move.catsling_rook) == str(fake_move.catsling_rook))
                    if decoded_move in self.state:
                        valid_input = decoded_move
                    else:
                        if self.turnning_player.simulation_flag:
                            message = 'simulated move - ' + str(decoded_move) + ' - for player ' + self.turnning_player.color + ' is invalid'
                            raise SimulationException(message)
                        else:
                            self.turnning_player.comm_output('invalid move', decoded_move)

            if isinstance(decoded_move, str):
                self.state = valid_input
            else:
                undo = self.board.execute_move(valid_input)

                self.record_history(valid_input)   # also records backtrack
                self.undo_stack.append(undo)
                self.whites_player.is_in_check = self.board.white_checked
                self.blacks_player.is_in_check = self.board.black_checked
                self.turnning_player, self.opposing_player = self.opposing_player, self.turnning_player
                self.semi_turn_count += 1
                self.turn_count = self.semi_turn_count//2 + 1

            if isinstance(self.state, list):
                self.state = self.determine_game_state()

            if verbose:
                self.turnning_player.comm_output(self.board)
                self.turnning_player.comm_output('state:', self.state)
                self.turnning_player.comm_output('-'*50)

        if self.state in ['exit', 'quit']:
            result = 'player ' + self.turnning_player.color + ' left the game'

        final_notation = self.full_notation()
        if self.state == 'stalemate':
            final_notation += '\n1/2-1/2'
            result = 'stalemate'

        if self.state in ['mate', 'forefit']:
            result = 'mate'
            if self.turnning_player == self.whites_player:
                final_notation += '\n0-1'
            else:
                final_notation += '\n1-0'

        if verbose:
            self.turnning_player.comm_output('result:', result)
            self.turnning_player.comm_output('notation:')
            self.turnning_player.comm_output(final_notation)
            self.turnning_player.comm_output('\nend position:')
            self.turnning_player.comm_output(self.board.export())

        return result