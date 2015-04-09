from piece import Piece
from move import Move, MoveException

EMPTYBOARD = {'a8':None, 'b8':None, 'c8':None, 'd8':None, 'e8':None, 'f8':None, 'g8':None, 'h8':None,
              'a7':None, 'b7':None, 'c7':None, 'd7':None, 'e7':None, 'f7':None, 'g7':None, 'h7':None,
              'a6':None, 'b6':None, 'c6':None, 'd6':None, 'e6':None, 'f6':None, 'g6':None, 'h6':None,
              'a5':None, 'b5':None, 'c5':None, 'd5':None, 'e5':None, 'f5':None, 'g5':None, 'h5':None,
              'a4':None, 'b4':None, 'c4':None, 'd4':None, 'e4':None, 'f4':None, 'g4':None, 'h4':None,
              'a3':None, 'b3':None, 'c3':None, 'd3':None, 'e3':None, 'f3':None, 'g3':None, 'h3':None,
              'a2':None, 'b2':None, 'c2':None, 'd2':None, 'e2':None, 'f2':None, 'g2':None, 'h2':None,
              'a1':None, 'b1':None, 'c1':None, 'd1':None, 'e1':None, 'f1':None, 'g1':None, 'h1':None,}

class Board():

    def __init__(self, construction_state={}):
        self.white = []
        self.black = []
        self.move_stack = []
        self.state = EMPTYBOARD.copy()
        if construction_state == {}:
            self.white_king = None
            self.black_king = None
            self.white_checked = False
            self.black_checked = False
        else:
            self.spawn_pieces(construction_state)

    def __repr__(self):
        result = '\n'
        for i in range(8,0,-1):
            result += '|'
            for j in range(97,105):
                piece = '  '
                try:
                    piece = self.state[chr(j)+str(i)].designation()
                except AttributeError:
                    pass
                result += piece + '|'
            result+='\n'
        return result

    def add_piece(self, color, type_, location):
        try: # for CT@XY
            type_ = color[1]
            location = color[-2:]
            color = color[0]
        except IndexError:
            pass

        if self.state[location]:
            message = 'Are you blind - there is another piece at that spot: ' + repr(self.state[location])
            raise MoveException(message)

        new_piece = Piece(color, type_, location)
        if new_piece.color == 'w':
            self.white.append(new_piece)
            if new_piece.type_ == 'k':
                self.white_king = new_piece
        else:
            self.black.append(new_piece)
            if new_piece.type_ == 'k':
                self.black_king = new_piece

        self.state[location] = new_piece

    def spawn_pieces(self, init_state):
        # 'state' here should be the input of the constructor, which should be dict of string values!
        for square in init_state.keys():
            if init_state[square] != '  ':
                self.add_piece(init_state[square][0], init_state[square][1], square)

        # self.white_checked = self.sq_in_check(self.wk,'b')
        # self.black_checked = self.sq_in_check(self.bk,'w')

    def lookup_by_square(self, square):
        pass
