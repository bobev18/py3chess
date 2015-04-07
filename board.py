from piece import Piece

EMPTYBOARD = {'a8':'  ', 'b8':'  ', 'c8':'  ', 'd8':'  ', 'e8':'  ', 'f8':'  ', 'g8':'  ', 'h8':'  ',
              'a7':'  ', 'b7':'  ', 'c7':'  ', 'd7':'  ', 'e7':'  ', 'f7':'  ', 'g7':'  ', 'h7':'  ',
              'a6':'  ', 'b6':'  ', 'c6':'  ', 'd6':'  ', 'e6':'  ', 'f6':'  ', 'g6':'  ', 'h6':'  ',
              'a5':'  ', 'b5':'  ', 'c5':'  ', 'd5':'  ', 'e5':'  ', 'f5':'  ', 'g5':'  ', 'h5':'  ',
              'a4':'  ', 'b4':'  ', 'c4':'  ', 'd4':'  ', 'e4':'  ', 'f4':'  ', 'g4':'  ', 'h4':'  ',
              'a3':'  ', 'b3':'  ', 'c3':'  ', 'd3':'  ', 'e3':'  ', 'f3':'  ', 'g3':'  ', 'h3':'  ',
              'a2':'  ', 'b2':'  ', 'c2':'  ', 'd2':'  ', 'e2':'  ', 'f2':'  ', 'g2':'  ', 'h2':'  ',
              'a1':'  ', 'b1':'  ', 'c1':'  ', 'd1':'  ', 'e1':'  ', 'f1':'  ', 'g1':'  ', 'h1':'  ',}

class Board():

    def __init__(self, state={}):
        self.white = []
        self.black = []
        self.move_stack = []
        if state == {}:
            self.white_king_location = ''
            self.black_king_location = ''
            self.white_checked = False
            self.black_checked = False
            self.state = EMPTYBOARD.copy()
        else:
            self.spawn_pieces(state)

    def __repr__(self):
        result = '\n'
        for i in range(8,0,-1):
            result += '|'
            for j in range(97,105):
                result += self.state[chr(j)+str(i)] + '|'
            result+='\n'
        return result

    def spawn_pieces(self, state):
        self.state = state.copy()
        # for square in self.state:
        #     if self.state[square] != '  ':
        #         if self.state[square][0]=='w':
        #             self.white.append(Piece(self.state[square][0], self.state[square][1], square))
        #             if self.state[square][1]=='k':
        #                 self.white_king_location = square
        #         else:
        #             self.black.append(Piece(self.state[square][0], self.state[square][1], square))
        #             if self.state[square][1]=='k':
        #                 self.black_king_location = square

        # self.white_checked = self.sq_in_check(self.wk,'b')
        # self.black_checked = self.sq_in_check(self.bk,'w')

    def lookup_by_square(self, square):
        pass
