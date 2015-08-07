from board import Board

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







class Game():

    def __init__(self, player1='human', player2='human', clock=60*60, board_position={}, logfile='d:/temp/chesslog.txt'):
        if board_position:
            self.board = Board(board_position)
        else:
            self.board = Board(INITIAL_POSITION)
        self.player1 = Player(player1, 'w', clock)
        self.player2 = Player(player2, 'b', clock)
        self.turnning_player = self.player1
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









