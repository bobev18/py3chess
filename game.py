from board import Board
from move import Move
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

'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8', 'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6', 'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5', 'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'


class Player():

    def __init__(self, type_, color, initial_clock_time, AI_depth = 0):
        self.type_ = type_
        self.color = color
        self.clock = initial_clock_time
        self.history = []
        self.is_in_check = False
        self.AI_depth = AI_depth
        self.moves_to_simulate = []

    def simulate(self, moves):
        self.moves_to_simulate = moves

    def comm_output(self, message):
        print(message)

    def comm_input(self, message):
        if self.moves_to_simulate:
            return self.moves_to_simulate.pop()
        else:
            return input(message)

    def prompt_input(self):
        # output(self.show()
        input_ = None
        while not input_:
            raw = self.comm_input('enter your move: ')
            try:
                input_ = self.decode_move(raw, )
            except MoveException as err:
                comm_output('erroneous move' + str(err.args))
                comm_output('enter "?" to view help')

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

        # return input_ #returns move or command

    def decode_move(self, raw_input_, piece_set, board_state):
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
            if not board_state[destination]:
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

        extra = board_state[destination]
        if promotion != '':
            move_type = 'p'
            extra = Piece(piece_set[0].color, promotion.lower(), destination)
            if capturing:
                move_type = '+'
                extra = [extra, board_state[destination]]
        if move_type == '':
            move_type = 'm'

        #list pieces matching the found type
        filtered = [ z for z in piece_set if z.type_ == piece_type.lower() ]
        if len(filtered)==0:
            message = 'no piece of the needed type (' + piece_type.lower() + ') is found in the piece set'
            raise MoveException(message)
        if len(filtered) == 1:
            return Move(filtered[0], move_type, destination, move_input, extra)

        # ----- STAGE 3 ----- #
        # #find if the move has disambiguation
        # disambiguation = ''
        # if capturing:
        #     if zmove[zmove.find(capture_sign)-1]!=piece_type: #true for pawn capture moves
        #         disambiguation = zmove[:zmove.find(capture_sign)-1] # the pawn file "cxd5"
        #     else:
        #         disambiguation = zmove[1:zmove.find(capture_sign)-1] # between first char (=piece type) and capture sign; i.e. Raxe4 -> 'a' or R8xe4 -> '8' or Re1xe4 -> 'e1' (has wr@e8, wr@a4 & wr@e1)
        #     if len(disambiguation)>2:
        #         raise MoveException('\n erroneous disambiguation '+disambiguation)
        # else:
        #     if len(destination)==3: # Rac1 = Rook from file "A" to "C1" ; N7g5 = Knight from rank "7" to "G5"
        #         disambiguation = destination[0]
        #         destination = destination[1:]
        #     elif len(destination)==4: # Nf7g5 differ from both Nh7 and Nf3 - you can have 3 pieces of same type after promotions
        #         disambiguation = destination[:2]
        #         if disambiguation not in board_state.keys():
        #             raise MoveException('disambiguation detected ('+disambiguation+'), but it is not on the board')
        #         destination = destination[2:]
        #         if destination not in board_state.keys():
        #             raise MoveException('destination detected as ('+destination+'), but it is not on the board')
        #     elif len(destination)>4:
        #         raise MoveException('\n erroneous destination '+destination)
        #     else:
        #         pass

        # if verbose >0:
        #     self.logit('disambigument:',disambiguation)
        #     self.logit('destination:',destination)

        # #filter by disambiguation
        # if len(disambiguation)>0:
        #     if len(disambiguation)==1:
        #         if disambiguation in [chr(x) for x in range(97,105)]:
        #             filtered = [ x for x in filtered if disambiguation == x.sq[0]] #disambiguation by file
        #         else:
        #             filtered = [ x for x in filtered if disambiguation == x.sq[1]] #disambiguation by rank
        #     else:
        #         filtered = [ x for x in filtered if disambiguation == x.sq] #disambiguation by origination square

        #     if len(filtered)==0:
        #         raise MoveException('no piece matching the disambiguation ('+disambiguation+') is found in the piece set')
        #     if len(filtered)==1:
        #         return (filtered[0],filtered[0].sq,move_type,destination,move)

        # #filter by destination
        # new = []
        # for x in filtered:
        #     exp_ = [z[1] for z in x.expand(board_state)]
        #     if verbose: self.logit(x,exp_)
        #     if destination in exp_:
        #         new.append(x)
        # filtered = new

        # if len(filtered)>1:
        #     raise MoveException('move is ambiguous. Possible executors:'+str(filtered))
        # if len(filtered)==0:
        #     raise MoveException('no piece expanding to the destination ('+destination+') is found in the piece set')
        # if verbose >0:  self.logit('result:',(filtered[0],(move_type,destination,move)))
        # return (filtered[0],filtered[0].sq,move_type,destination,move)







class Game():

    def __init__(self, whites_player_type='human', blacks_player_type='human', clock=60*60, board_position={}, logfile='d:/temp/chesslog.txt'):
        if board_position:
            self.board = Board(board_position)
        else:
            self.board = Board(INITIAL_POSITION)
        self.whites_player = Player(whites_player_type, 'w', clock)
        self.blacks_player = Player(blacks_player_type, 'b', clock)
        self.turnning_player = self.whites_player
        self.turn_count = 1
        self.undo_stack = []
        self.full_notation = '' # quite as the values in hist, but with the count and # + ? !
        self.state = 'init'
        with open(logfile,'w') as f:
            self.logfile = logfile

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
        result=[]
        # for piece in self.board.pieces_of_color(self.turnning_player.color):
        #     ------------------->
        #     temporary_result = self.verified(p,verbose)
        #     rez.extend(temp_rez)
        #     if verbose>0:
        #         print 'p',p,'rez',temp_rez

        # if verbose>1:
        #     print 'mate rez (all avail moves for the pl in turn):', rez
        # if verbose>0:
        #     print 'len avail moves:', len(rez)

        # if len(rez)==0:
        #     if verbose>0:
        #         print 'player on turn is ',self.turn['col'],' and check against him is :',self.turn['is_in_check']
        #     if self.turn['is_in_check']:
        #         return 'mate'
        #     else:
        #         return 'stalemate'
        # else:
        #     # repeated moves
        #     if len(self.zboard.backtrack)>0 and self.zboard.backtrack.count(self.zboard.backtrack[-1])>=3:
        #         if verbose>0:
        #             print 'backtrack',self.zboard.backtrack
        #         return 'stalemate'
        #     return ''

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





    def start(self):
        # self.state = 'active'
        # check if initial position is mate or stalemate i.e. active
        self.state = self.mate()
        while self.state == 'active':
            valid_input = False
            while not valid_input:
                input_ = self.turnning_player.prompt_input()
            #     valid_input = __validate_against_z3levels__(input_)
            #     # input could affect the cycle in three ways:
            #     # 1. valid move to pass turn to the other player
            #     # 2. valid command that keeps move (i.e. show info, export, undo, etc)
            #     # 3. valid command affecting game state - offer draw, surrender, quit
            #     if valid_input in ['info', 'export', 'undo']:
            #         anction_input(valid_input)
            #         valid_input = False

            # if valid_input not in ['offer draw', 'surrender', 'quit']
            #     execute_move(valid_input)
            #     self.undo_stack.append(valid_input__or__derivate)
            #     if self.turnning_player == self.player1:
            #         self.turnning_player = self.player2
            #     else:
            #         self.turnning_player = self.player1
            #     self.turn_count += 1
            #     self.full_notation += self.notator(valid_input)
            #     self.history.append(valid_input) #list?
            # else:
            #     self.state = valid_input

            # self.state = self.mate()

        if self.state == 'stalemate':
            self.full_notation += '\n1/2-1/2'
            result = 'stalemate'

        return result








