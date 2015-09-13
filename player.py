import re
from move import Move
from board import CAPTURE_SIGN

CORE_NOTATION_PATTERN = re.compile(r'(?P<piece_type>[NBRQK]?)(?P<disambiguation>[a-h]?\d?)(?P<capture_sign>' + \
            CAPTURE_SIGN + '?)(?P<destination>[a-h]\d)(?P<promotion>[NBRQ]?)')

COMMANDS = ['', '?', 'help', 'history', 'notation', 'export', 'undo', 'quit', 'exit', 'draw', 'forefit']

class DecodeException(Exception):
    # to handle as "invalid input"
    def __init__(self, *args):
        self.args = [a for a in args]

class MoveExhaustException(Exception):
    # to handle exhaust of simulated moves
    def __init__(self, *args):
        self.args = [a for a in args]

class Player():

    def __init__(self, game, type_, color, initial_clock_time, AI_depth = 0):
        self.type_ = type_
        self.color = color
        self.clock = initial_clock_time
        # self.history = []
        self.is_in_check = False
        self.AI_depth = AI_depth
        self.moves_to_simulate = []
        self.simulation_flag = False
        self.game = game

    def simulate(self, moves):
        self.moves_to_simulate = moves
        self.simulation_flag = True

    def comm_output(self, *args):
        print(*args)

    def comm_input(self, message):
        if len(self.moves_to_simulate):
            return self.moves_to_simulate.pop(0)
        else:
            if not self.simulation_flag:
                try:
                    return input(message)
                except EOFError as error:
                    return None

    def prompt_input(self):
        # output(self.show()
        input_ = None
        while not input_:
            raw = self.comm_input('enter your move: ')
            if not raw:
                message = 'player ' + self.color + ' exhausted simulated moves'
                raise MoveExhaustException(message)
            if raw in COMMANDS:
                if raw in ['?', 'help']:
                    self.comm_output('commands:')
                    self.comm_output('notation - show game notation')
                    self.comm_output('export - show position as dictionary, and move history as list')
                    # self.comm_output('verbose - toggle verbose on and off')
                    self.comm_output('undo - revert full turn')
                    self.comm_output('draw - offer draw, also accept draw if offered')
                    self.comm_output('forefit - give up')
                    self.comm_output('exit - exit the game')
                    # self.comm_output('advanced: ?eval(...) ; ?preval(...) - the second executes in the game cycle(for better scope)')
                elif raw in ['history', 'notation']:
                    self.comm_output(self.game.full_notation())
                elif raw in ['exit', 'quit', 'draw', 'forefit']:
                    input_ = raw
                elif raw == 'export':
                    self.comm_output(self.game.board.export())
                    self.comm_output(self.game.history)
                elif raw == 'undo':
                    self.game.undo_last()
                    if not self.simulation_flag:
                        self.comm_output(self.game.board)
                else:
                    self.comm_output('enter "?" to view help')

            else:
                try:
                    # input_ = self.game.decode_move(raw, self.game.board.pieces_of_color(self.color))
                    input_ = self.decode_move(raw) #, self.game.board.pieces_of_color(self.color))
                except DecodeException as error:
                    if self.simulation_flag:
                        raise
                    else:
                        self.comm_output('erroneous move' + str(error.args))
                        self.comm_output('enter "?" to view help')

        return input_ #returns move or command

    def decode_move(self, _input_):
        piece_set = self.game.board.pieces_of_color(self.color)

        debug_verbosing = False
        # debug_verbosing = True
        # print('rawest raw:', _input_)

        core_move_notation_matches = re.findall(r'\d{0,3}\.{0,3}\s?(.+?)[\?\!\+#]?$', _input_)
        if not len(core_move_notation_matches):
            message = 'failed to extract core move notation from input - ' + _input_
            raise DecodeException(message)
        core_move_notation = core_move_notation_matches[0]
        move_input = core_move_notation.strip()

        # ----- STAGE 1 ----- #
        # rule out casteling
        if move_input.count('O') == 2 or move_input.count('0') == 2: #king side castle
            king_piece = [ z for z in piece_set if z.type_ == 'k' ][0]
            destination = 'g' + king_piece.location[1] #the rank of king - could be 1 or 8
            rook = [ z for z in piece_set if z.type_ == 'r' and z.location == ('h' + king_piece.location[1]) ][0]
            return Move(king_piece, 'c', destination, 'O-O', rook)

        if move_input.count('O') == 3 or move_input.count('0') == 3: #queen side castle
            king_piece = [ z for z in piece_set if z.type_ == 'k' ][0]
            destination = 'c' + king_piece.location[1]
            rook = [ z for z in piece_set if z.type_ == 'r' and z.location == ('a' + king_piece.location[1]) ][0]
            return Move(king_piece, 'c', destination, 'O-O-O', rook)

        if debug_verbosing: print('past stage 1', move_input, ' (means no casteling)')

        # ----- STAGE 2 ----- #
        # filter by piece type
        move_matches = CORE_NOTATION_PATTERN.match(move_input)
        if not move_matches:
            message = 'failed to parse move notation from core_notation - ' + move_input + '(raw: ' + _input_ + ')'
            raise DecodeException(message)
        piece_type = move_matches.group('piece_type').lower()
        if not len(piece_type):
            piece_type = 'p'
        disambiguation = move_matches.group('disambiguation')
        capturing = move_matches.group('capture_sign') != ''
        destination = move_matches.group('destination')
        promotion = move_matches.group('promotion').upper()

        if capturing:
            if promotion != '':
                move_type = '+'
                extra = [promotion, self.game.board.state[destination]]
            else:
                move_type = 't'
                extra = self.game.board.state[destination] 
                if not extra:
                    if piece_type == 'p' and destination[1] in ['3','6']:
                        enpassan = True
                        move_type='e'
                        if destination[1] == '3':
                            taken_location = destination[0] + '4'
                        else:
                            taken_location = destination[0] + '5'
                        extra = self.game.board.state[taken_location]
                    else:
                        message = 'taking empty spot ' + destination + ', by non pawn - ' + piece_type + '(no possible en passant)'
                        raise DecodeException(message)
        else:
            if promotion != '':
                move_type = 'p'
                extra = promotion
            else:
                move_type = 'm'
                extra = None
        
        relevant_pieces = [ z for z in piece_set if z.type_ == piece_type ]
        if len(relevant_pieces) == 0:
            message = 'no piece of the needed type (' + piece_type + ') is found in the piece set'
            raise DecodeException(message)
        if len(relevant_pieces) == 1:
            return Move(relevant_pieces[0], move_type, destination, move_input, extra)

        if debug_verbosing: print('stage 2: filtered pieces', relevant_pieces, 'extra', extra, 'type', move_type, 'piece_type', piece_type)

        # ----- STAGE 3 ----- #
        # filter by disambiguation
        if len(disambiguation):
            if len(disambiguation) == 1:
                if disambiguation in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                    relevant_pieces = [ z for z in relevant_pieces if disambiguation == z.location[0]] # by file
                else:
                    relevant_pieces = [ z for z in relevant_pieces if disambiguation == z.location[1]] # by rank
            if len(disambiguation) == 2:
                relevant_pieces = [ z for z in relevant_pieces if disambiguation == z.location] # by origin
        
            if len(relevant_pieces) == 0:
                message = 'no piece matching the disambiguation (' + disambiguation + ') is found in the piece set'
                raise DecodeException(message)
            if len(relevant_pieces) == 1:
                return Move(relevant_pieces[0], move_type, destination, move_input, extra)

        if debug_verbosing: print('stage 3: filtered pieces', relevant_pieces)

        # ----- STAGE 4 ----- #
        # filter by matching input against generated moves (for the remaining piece candidates)
        notation_filtered = []
        for candidate_piece in relevant_pieces:
            expansions = [ z for z in self.game.board.naive_moves(candidate_piece) if z.notation == move_input ]
            notation_filtered.extend(expansions)
        if len(notation_filtered) == 0:
            message = 'input ' + move_input + ' does not match any of the notations generated for the relevant pieces (' + str([ z.notation for z in notation_filtered ]) + ')'
        elif len(notation_filtered) == 1:
            return notation_filtered[0]
        else:
            message = 'the move is ambiguous. Possible interpretations:' + str(notation_filtered)
        raise DecodeException(message)
