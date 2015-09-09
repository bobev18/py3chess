from board import Board
from move import Move, MoveException
from piece import Piece
import re

from board import CAPTURE_SIGN

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

class Player():

    def __init__(self, game, type_, color, initial_clock_time, AI_depth = 0):
        self.type_ = type_
        self.color = color
        self.clock = initial_clock_time
        self.history = []
        self.is_in_check = False
        self.AI_depth = AI_depth
        self.moves_to_simulate = []
        self.game = game

    def simulate(self, moves):
        self.moves_to_simulate = moves

    def comm_output(self, message):
        print(message)

    def comm_input(self, message):
        if self.moves_to_simulate:
            return self.moves_to_simulate.pop(0)
        else:
            return input(message)

    def prompt_input(self):
        # output(self.show()
        input_ = None
        while not input_:
            raw = self.comm_input('enter your move: ')
            input_ = self.game.decode_move(raw, self.game.board.pieces_of_color(self.color))

            # try:
            #     input_ = self.game.decode_move(raw, self.game.board.pieces_of_color(self.color))
            # except MoveException as err:
            #     self.comm_output('erroneous move' + str(err.args))
            #     self.comm_output('enter "?" to view help')

        #     if len(inp)>0 and inp[0] != '?':
        #         try:
        #             input_ = self.decode_move(inp,self.turnset())
        #         except MoveException as err:
        #             print 'erroneous move',err.args
        #             print 'enter "?" to view commands'
        #     elif inp[0] == '?':
        #         if inp == '?' or inp == '?help':
        #             print 'commands:\n?hist - show game notation\n?export - print position as dict\n?verbose - tongle verbose on and off\n?undo - revert full turn\n?exit - exit the game'
        #             print 'advanced: ?eval(...) ; ?preval(...) - the second executes in the game cycle(for better scope)'
        #             inp = None
        #         elif inp.count('?eval')>0:
        #             print eval(inp[6:-1])
        #             inp = None
        #         elif inp.count('?preval')>0:
        #             input_ = inp[3:]
        #         else:
        #             input_ = inp[1:]
        #     else:
        #         pass

        return input_ #returns move or command





class Game():

    def __init__(self, whites_player_type='human', blacks_player_type='human', clock=60*60, board_position={}, logfile='d:/temp/chesslog.txt'):
        if board_position:
            self.board = Board(board_position)
        else:
            self.board = Board(INITIAL_POSITION)
        self.whites_player = Player(self, whites_player_type, 'w', clock)
        self.blacks_player = Player(self, blacks_player_type, 'b', clock)
        self.turnning_player = self.whites_player
        self.turn_count = 1
        self.undo_stack = []
        self.full_notation = '' # quite as the values in hist, but with the count and # + ? !
        self.history = []       # to be used for checks of past Moves
        self.state = 'init'
        with open(logfile,'w') as f:
            self.logfile = logfile

    def decode_move(self, raw_input_, piece_set): #, board_state):
        # capture turn count if included in notation

        # ----- STAGE 1 ----- #
        # move_number = re.search(r'\d{1,3}\.{0,3}\s?', raw_input_)
        move_number = re.match(r'\d{1,3}\.{0,3}\s?', raw_input_)
        if move_number == None:
            move_input = raw_input_
        else:
            # print(move_number, move_number.start(), move_number.end())
            move_input = raw_input_[move_number.end():]

        #clean punctuation, #clean/process end chars
        if move_input.count('?')>0:
            move_input = move_input[:move_input.find('?')]
        if move_input.count('!')>0:
            move_input = move_input[:move_input.find('!')]
        if move_input.count('+')>0:
            move_input = move_input[:move_input.find('+')] # check & double check
        if move_input.count('#')>0:
            move_input = move_input[:move_input.find('#')] # mate

        move_input = move_input.strip()
        history_notation = move_input # this is the format for the notation we track in the hist
        promotion = '' #promoting a pawn i.e. e8Q
        for possible_promotion in ['R','N','B','Q']:
            if move_input[-1] == possible_promotion:
                promotion = possible_promotion
        if promotion != '':
            move_input = move_input[:-1] #clean the promo character, to avoid mistake in piece dicovery

        #casteling
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


        # print('past stage1', move_input)

        # ----- STAGE 2 ----- #
        # determine piece type
        piece_type = 'p'
        for possible_piece_type in ['R','N','B','Q','K']:
            if move_input.count(possible_piece_type)>0:
                piece_type = possible_piece_type
            if move_input.count(possible_piece_type)>1:
                message = 'more than one reference to piece type ' + possible_piece_type + ' is found in the notation ' + move_notation
                raise MoveException(message)

        # determine move type
        move_type = ''
        enpassan = False
        if move_input.count(CAPTURE_SIGN)>0:
            capturing = True
            move_type='t'
            destination = move_input[move_input.find(CAPTURE_SIGN)+1:]
            if destination not in INITIAL_POSITION.keys():
                message = 'capture sign detected in move, but destination (' + destination + ') is not on the board'
                raise MoveException(message)
            if not self.board.state[destination]:
                if piece_type == 'p' and destination[1] in ['3','6']:
                    enpassan = True #possibility yet -- will get verified through matching expansion
                    move_type='e'
                else:
                    message = 'taking empty spot ' + destination + ', by non pawn - ' + piece_type + '(no possible en passant)'
                    raise MoveException(message)
        else:
            capturing = False
            if move_input.count(piece_type)>0:
                destination = move_input[move_input.find(piece_type)+1:]
            else:
                destination = move_input

        extra = self.board.state[destination]
        if promotion != '':
            move_type = 'p'
            extra = Piece(piece_set[0].color, promotion.lower(), destination)
            if capturing:
                move_type = '+'
                extra = [extra, self.board.state[destination]]
        if move_type == '':
            move_type = 'm'

        #list pieces matching the found type
        filtered = [ z for z in piece_set if z.type_ == piece_type.lower() ]
        if len(filtered) == 0:
            message = 'no piece of the needed type (' + piece_type.lower() + ') is found in the piece set'
            raise MoveException(message)
        if len(filtered) == 1:
            return Move(filtered[0], move_type, destination, move_input, extra)

        # print('stage 2', filtered)

        # ----- STAGE 3 ----- #
        # find if the move has disambiguation
        disambiguation = ''
        if capturing:
            if move_input[move_input.find(CAPTURE_SIGN)-1] != piece_type: #true for pawn capture moves
                disambiguation = move_input[:move_input.find(CAPTURE_SIGN)-1] # the pawn file "cxd5"
            else:
                disambiguation = move_input[1:move_input.find(CAPTURE_SIGN)-1] # between first char (=piece type) and capture sign; i.e. Raxe4 -> 'a' or R8xe4 -> '8' or Re1xe4 -> 'e1' (has wr@e8, wr@a4 & wr@e1)
            if len(disambiguation) > 2:
                message = '\n erroneous disambiguation ' + disambiguation
                raise MoveException(message)
        else:
            if len(destination) == 3: # Rac1 = Rook from file "A" to "C1" ; N7g5 = Knight from rank "7" to "G5"
                disambiguation = destination[0]
                destination = destination[1:]
            elif len(destination) == 4: # Nf7g5 differ from both Nh7 and Nf3 - you can have 3 pieces of same type after promotions
                disambiguation = destination[:2]
                if disambiguation not in self.board.state.keys():
                    message = 'disambiguation detected (' + disambiguation + '), but it is not on the board'
                    raise MoveException(message)
                destination = destination[2:]
                if destination not in self.board.state.keys():
                    message = 'destination detected as (' + destination + '), but it is not on the board'
                    raise MoveException(message)
            elif len(destination) > 4:
                message = '\n erroneous destination ' + destination
                raise MoveException(message)
            else:
                pass

        #filter by disambiguation
        if len(disambiguation) > 0:
            if len(disambiguation) == 1:
                if disambiguation in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                    filtered = [ z for z in filtered if disambiguation == z.location[0]] #disambiguation by file
                else:
                    filtered = [ z for z in filtered if disambiguation == x.location[1]] #disambiguation by rank
            else:
                filtered = [ z for z in filtered if disambiguation == x.location] #disambiguation by origination square

            if len(filtered) == 0:
                message = 'no piece matching the disambiguation (' + disambiguation + ') is found in the piece set'
                raise MoveException(message)
            if len(filtered) == 1:
                return Move(filtered[0], move_type, destination, move_input, extra)

        # print('stage 3', filtered)

        # ----- STAGE 4 ----- #
        # filter by matching generated moves (for the remaining candidates) to the input
        destination_filtered = []
        for candidate_piece in filtered:
            expansions = [ z for z in self.board.naive_moves(candidate_piece) if z.destination == destination ]
            destination_filtered.extend(expansions)
        if len(destination_filtered) == 0:
            message = 'no piece expanding to the decoded destination (' + destination + ') is found in the piece set'
            raise MoveException(message)
        elif len(destination_filtered) == 1:
            return destination_filtered[0]
        else:
            extra_filtered = [ z for z in destination_filtered if z.promote_to == promotion ]

            if len(extra_filtered) == 0:
                message = 'no promotions (' + str([ z.promote_to for z in extra_filtered ]) + '), match the decoded promotion: ' + promotion
                raise MoveException(message)
            elif len(extra_filtered) == 1:
                return extra_filtered[0]
            else:
                message = 'the move is ambiguous. Possible interpretations:' + str(extra_filtered)
                raise MoveException(message)

        message = 'end of the "decode_move" method - this should be unreachable code '
        raise MoveException(message)

    def mate(self):
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
        result = []
        for piece in self.board.pieces_of_color(self.turnning_player.color):
            temporary_result = self.valid_moves_of_piece_at(piece.location)
            result.extend(temporary_result)

        if len(result) == 0:
            if self.turnning_player.is_in_check:
                return 'mate'
            else:
                return 'stalemate'
        else:
            # repeated moves
            if len(self.history) > 0 and self.board.backtrack.count(self.board.backtrack[-1]) >= 3:
                return 'stalemate'

        return 'active'

    def valid_moves_of_piece_at(self, location):
        result = []
        for move in self.board.naive_moves(self.board.state[location]):
            # test_state = deepcopy(self.board)
            # print(type(test_state), test_state)
            # print('validating move', move)
            # test_state.execute_move(move)
            # if test_state.validate_move(move):
            #     result.append(move)
            # # the above fails because the Piece obj referenced in the Move obj is not the same as the one in the copy's white/black piece list

            # undo = self.board.execute_move(move)
            # print(undo)
            # if self.board.validate_move(move):
            #     result.append(move)
            # self.board.undo_actions(undo)
            ### aparently 'execute_move' incorporates the validate_move check

            undo = self.board.execute_move(move)
            if undo:
                result.append(move)
                self.board.undo_actions(undo)

        return result

    def valid_move(self, move):
        undo = self.board.execute_move(move)
        if undo:
            self.board.undo_actions(undo)
            return True
        return False

    def notator(self, move):
        if self.turnning_player == self.whites_player:
            return str(self.turn_count) + '. ' + move.notation
        else:
            return '  ' + move.notation + '\n'

    def start(self, verbose = True):
        # self.state = 'active'
        # check if initial position is mate or stalemate i.e. active
        self.state = self.mate()
        while self.state == 'active':
            valid_input = False
            while not valid_input:
                input_ = self.turnning_player.prompt_input()
                if self.valid_move(input_):
                    valid_input = input_

            #     # input could affect the cycle in three ways:
            #     # 1. valid move to pass turn to the other player
            #     # 2. valid command that keeps move (i.e. show info, export, undo, etc)
            #     # 3. valid command affecting game state - offer draw, surrender, quit
            #     if valid_input in ['info', 'export', 'undo']:
            #         anction_input(valid_input)
            #         valid_input = False

            if valid_input not in ['offer draw', 'surrender', 'quit']:
                undo = self.board.execute_move(valid_input)
                self.undo_stack.append(undo)
                self.whites_player.is_in_check = self.board.white_checked
                self.blacks_player.is_in_check = self.board.black_checked
                if self.turnning_player == self.whites_player:
                    self.turnning_player = self.blacks_player
                else:
                    self.turnning_player = self.whites_player
                self.turn_count += 1
                self.full_notation += self.notator(valid_input)
                self.history.append(valid_input) #list?
            else:
                self.state = 'valid_input'

            self.state = self.mate()
            if verbose:
                print(self.board)
                print('state:', self.state)
                print('-'*50)

        if self.state == 'stalemate':
            self.full_notation += '\n1/2-1/2'
            result = 'stalemate'

        if self.state == 'mate':
            result = 'mate'
            if self.turnning_player == self.whites_player:
                self.full_notation += '\n1-0'
            else:
                self.full_notation += '\n0-1'

        if verbose:
            print('result:', result)

        return result









