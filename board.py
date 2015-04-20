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
                try:
                    piece = self.state[chr(j)+str(i)].designation()
                except AttributeError:
                    piece = '  '
                result += piece + '|'
            result+='\n'
        return result

    def add_piece(self, color, type_='', location=''):
        if isinstance(color, Piece):
            new_piece = color
            location = new_piece.location
        else:
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

    def remove_piece(self, location):
        if isinstance(location, Piece):
            piece = location
        else:
            piece = self.state[location]

        if not piece:
            message = 'Trying to move the air at ' + location
            raise MoveException(message)

        self.state[location] = None
        if piece.color == 'w':
            self.white.remove(piece)
        else:
            self.black.remove(piece)

    def relocate(self, from_, to):
        if isinstance(from_, Piece):
            piece = from_
            # from_ = piece.location  ## altering value here, may also change it on a higher level if the obj is mutable
            origin = piece.location
        else:
            piece = self.state[from_]
            origin = from_

        if self.state[to]:
            msg = 'Are you blind - there is another piece at that spot: ' + repr(self.state[to])
            raise MoveException(msg)

        piece.location = to
        piece.x = ord(piece.location[0])-96
        piece.y = int(piece.location[1])

        self.state[to] = piece
        self.state[origin] = None

    def naive_moves(self, piece):
        preliminary = piece.lookup_moves()
        results = []

        # moving to empty square
        for destination in preliminary['m']:
            if not self.state[destination]:
                results.append(Move(piece, 'm', destination, piece.notation + destination))

        # for pawn jumps over empty square
        for destination in preliminary['m2']:
            if not self.state[destination] and ((piece.color == 'w' and not self.state[destination[0]+'3']) or (piece.color == 'b' and not self.state[destination[0]+'6'])):
                results.append(Move(piece, 'm2', destination, piece.notation + destination))

        # taking non empty square
        for destination in preliminary['t']:
            if self.state[destination].color != piece.color:
                if piece.notation == '':
                    results.append(Move(piece, 't', destination, piece.location[0] + capture_sign + destination))
                else:
                    results.append(Move(piece, 't', destination, piece.notation + capture_sign + destination))

        # promote on empty
        for destination in preliminary['p']:
            if not self.state[destination[:2]]:
                results.append(Move(piece, 'p', destination[:2], destination, ))
                rez.append(('p',destination[:2],destination))

        # capture-promote on non empty
        for destination in preliminary['+']:
            if self.state[destination[:2]][0]==oppcol:
                if pdesignation=='':
                    pdesignation = self.sq[0]
                rez.append(('+',destination[:2],pdesignation+capture_sign+destination))

        # en passant - destination empty, side non empty of opposite color
        for destination in preliminary['e']:
            if self.state[destination]=='  ' and self.state[destination[0]+self.sq[1]]==oppcol+'p':
                pdesignation = self.sq[0]
                rez.append(('e',destination,pdesignation+capture_sign+destination))

        # castle - all
        for destination in preliminary['c']:
            if self.state[destination]=='  ':
                if destination[0]=='g':
                    if self.state['f'+self.sq[1]]=='  ' and self.state['g'+self.sq[1]]=='  ' and self.state['h'+self.sq[1]]== self.col+'r':
                        rez.append(('c',destination,'O-O'))
                else:
                    if self.state['b'+self.sq[1]]=='  ' and self.state['c'+self.sq[1]]=='  ' and self.state['d'+self.sq[1]]=='  ' and self.state['a'+self.sq[1]]== self.col+'r':
                        rez.append(('c',destination,'O-O-O'))

        #
        for direct in ['NE','SE','SW','NW','N','E','S','W']:
            for destination in preliminary[direct]:
                if self.state[destination]=='  ':
                    rez.append(('m',destination,pdesignation+destination))
                else:
                    if self.state[destination][0]==oppcol:
                        rez.append(('t',destination,pdesignation+capture_sign+destination))
                    break

        return rez


