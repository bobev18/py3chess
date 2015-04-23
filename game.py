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

    def comm_output(self, message):
        print(message)

    def comm_input(self, message):
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

    def __init__(self, player1='human', player2='human', clock=60*60, logfile='d:/temp/chesslog.txt'):
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

    def start(self):
        self.state = 'active'
        while self.state == 'active':
            valid_input = False
            while not valid_input:
                input_ = self.turnning_player.prompt_input()





