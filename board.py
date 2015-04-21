from piece import Piece
from move import Move, MoveException

CAPTURE_SIGN = 'x'

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
        results = []
        preliminary = piece.lookup_moves()
        for move_type in ['m','m2','mk','t','p','+','e','c','NE','SE','SW','NW','N','E','S','W']:
            if not move_type in preliminary.keys():
                preliminary[move_type] = []

        # moving to empty square
        for destination in preliminary['m']:
            if not self.state[destination]:
                results.append(Move(piece, 'm', destination, destination))

        # for pawn jumps over empty square
        for destination in preliminary['m2']:
            if not self.state[destination] and ((piece.color == 'w' and not self.state[destination[0]+'3']) or (piece.color == 'b' and not self.state[destination[0]+'6'])):
                results.append(Move(piece, 'm2', destination, destination))

        # moving K to empty square
        for destination in preliminary['mk']:
            if not self.state[destination]:
                results.append(Move(piece, 'mk', destination, piece.notation() + destination))

        # taking non empty square
        for destination in preliminary['t']:
            if self.state[destination] and self.state[destination].color != piece.color:
                results.append(Move(piece, 't', destination, piece.notation() + CAPTURE_SIGN + destination))

        # promote on empty
        for destination in preliminary['p']:
            if not self.state[destination]:
                for option in ['N', 'B', 'R', 'Q']:
                    results.append(Move(piece, 'p', destination, destination + option, option))

        # capture-promote on non empty
        for destination in preliminary['+']:
            if self.state[destination] and self.state[destination].color != piece.color:
                for option in ['N', 'B', 'R', 'Q']:
                    results.append(Move(piece, '+', destination, piece.notation() + CAPTURE_SIGN + destination + option, option))

        # en passant - destination empty, side non empty of opposite color
        for destination in preliminary['e']:
            opponent = self.state[destination[0] + piece.location[1]]
            if opponent and opponent.color != piece.color and opponent.type_ == 'p' and not self.state[destination]:
                results.append(Move(piece, 'e', destination, piece.notation() + CAPTURE_SIGN + destination))

        # castle - all
        for destination in preliminary['c']:
            if not self.state[destination]:
                if piece.color == 'w':
                    if destination[0] == 'g' and self.state['h1'] and self.state['h1'].designation() == 'wr' and not self.state['f1']:
                        results.append(Move(piece, 'c', destination, 'O-O'))
                    if destination[0] == 'c' and self.state['a1'] and self.state['a1'].designation() == 'wr' and not self.state['d1'] and not self.state['b1']:
                        results.append(Move(piece, 'c', destination, 'O-O-O'))
                else:
                    if destination[0] == 'g' and self.state['h8'] and self.state['h8'].designation() == 'br' and not self.state['f8']:
                        results.append(Move(piece, 'c', destination, 'O-O'))
                    if destination[0] == 'c' and self.state['a8'] and self.state['a8'].designation() == 'br' and not self.state['d8'] and not self.state['b8']:
                        results.append(Move(piece, 'c', destination, 'O-O-O'))

        #
        for direction in ['NE','SE','SW','NW','N','E','S','W']:
            for destination in preliminary[direction]:
                if not self.state[destination]:
                    results.append(Move(piece, 'm', destination, piece.notation() + destination))
                else:
                    if self.state[destination].color != piece.color:
                        results.append(Move(piece, 't', destination, piece.notation() + CAPTURE_SIGN + destination))
                    break

        return results


