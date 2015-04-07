import unittest

from piece import Piece
from move import Move, MoveException
from board import Board

TEST_POSITION1 = {'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': 'wp', 'h4': '  ', 'h5': '  ', 'd8': 'bq', 'a8': 'br', 'd6': '  ', 'd7': 'bp', 'd4': '  ', 'd5': '  ', 'd2': 'wp', 'd3': '  ', 'd1': 'wq', 'g7': 'bp', 'g6': '  ', 'g5': 'wp', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': 'bn', 'c8': 'bb', 'c3': 'bn', 'c2': 'wp', 'c1': 'wb', 'c7': 'bp', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': 'wb', 'f2': 'wp', 'f3': '  ', 'f4': '  ', 'f5': 'bp', 'f6': '  ', 'f7': '  ', 'f8': 'bb', 'b4': '  ', 'b5': '  ', 'b6': '  ', 'b7': 'bp', 'b1': 'wn', 'b2': 'wp', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': 'wp', 'a5': '  ', 'e8': 'bk', 'a7': 'bp', 'a6': '  ', 'e5': '  ', 'e4': 'wn', 'e7': 'bp', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': 'wp', 'a4': '  '}
POSITION1_VIEW = """
|br|  |bb|bq|bk|bb|bn|  |
|bp|bp|bp|bp|bp|  |bp|wp|
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |bp|wp|  |
|  |  |  |  |wn|  |  |  |
|  |  |bn|  |  |  |  |  |
|wp|wp|wp|wp|wp|wp|  |  |
|wr|wn|wb|wq|wk|wb|  |wr|
"""

class PieceTest(unittest.TestCase):

    def test_piece_initialization(self):
        test_piece = Piece('w', 'p', 'e2')
        self.assertEqual('wp@e2',repr(test_piece))

    def test_lookup_moves_on_empty_board(self):
        test_piece = Piece('w', 'p', 'e2')
        self.assertEqual({'m': ['e3'], 't': ['d3', 'f3'], 'm2': ['e4']}, test_piece.lookup_moves())

        test_piece = Piece('w', 'p', 'e8')
        self.assertEqual({}, test_piece.lookup_moves())

class MoveTest(unittest.TestCase):

    def test_move_initialization(self):
        test_piece = Piece('w', 'p', 'e2')
        test_move = Move(test_piece, 'e2', 'm2', 'e4', 'e4')
        self.assertEqual('e4',repr(test_move))

        # ensure piece location matches the move origin
        test_piece = Piece('w', 'p', 'e2')
        self.assertRaises(MoveException, Move, test_piece, 'e4', 'm', 'e5', 'e5')

class BoardTest(unittest.TestCase):

    def test_board_initialization(self):
        test_board = Board(TEST_POSITION1)
        self.assertEqual(POSITION1_VIEW,repr(test_board))
        # self.assertEqual('wn@e4', repr(test_board.lookup_by_square('e4')))





if __name__ == "__main__":
    try: unittest.main()
    except SystemExit: pass






# class boardTest(unittest.TestCase):

#     #init
#     zboard = chesslib.board()

#     def test_show(self):
#         self.zboard.initialset()
#         zshow = self.zboard.show()
#         #print(zshow)
#         self.assertEqual("""|br|bn|bb|bq|bk|bb|bn|br|
# |bp|bp|bp|bp|bp|bp|bp|bp|
# |  |  |  |  |  |  |  |  |
# |  |  |  |  |  |  |  |  |
# |  |  |  |  |  |  |  |  |
# |  |  |  |  |  |  |  |  |
# |wp|wp|wp|wp|wp|wp|wp|wp|
# |wr|wn|wb|wq|wk|wb|wn|wr|
# """,zshow)

#     def test_piecebypos_n_posbypiece_n_repr(self):
#         self.zboard.initialset()
#         zpiece = self.zboard.piece_by_sq('e2')
#         self.assertEqual('wp@e2',repr(zpiece))
#         zpos = zpiece.sq
#         self.assertEqual('e2',zpos)

#     def test_moves_n_takes(self):
#         self.zboard.initialset()
#         self.zboard.relocate('b8','c3')
#         #print(self.zboard.show())
#         self.zboard.relocate('g1','e4')
#         self.zboard.relocate('g2','g5')
#         self.zboard.relocate(self.zboard.piece_by_sq('f7'),'f5')
#         self.zboard.take(self.zboard.piece_by_sq('h7'))
#         self.assertEqual(None,self.zboard.piece_by_sq('h7')) # have to assert before moving another piece over to the same square
#         self.zboard.take(self.zboard.piece_by_sq('h8'))
#         self.zboard.relocate(self.zboard.piece_by_sq('h2'),'h7')

#         #print(self.zboard.show())
#         self.assertEqual('bn@c3',repr(self.zboard.piece_by_sq('c3')))
#         self.assertEqual('wn@e4',repr(self.zboard.piece_by_sq('e4')))
#         self.assertEqual('wp@g5',repr(self.zboard.piece_by_sq('g5')))
#         self.assertEqual('bp@f5',repr(self.zboard.piece_by_sq('f5')))
#         self.assertEqual(None,self.zboard.piece_by_sq('h8'))
#         self.assertEqual('wp@h7',repr(self.zboard.piece_by_sq('h7')))

#     def test_piecefy(self):
#         self.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': 'wp', 'h4': '  ', 'h5': '  ', 'd8': 'bq', 'a8': 'br', 'd6': '  ', 'd7': 'bp', 'd4': '  ', 'd5': '  ', 'd2': 'wp', 'd3': '  ', 'd1': 'wq', 'g7': 'bp', 'g6': '  ', 'g5': 'wp', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': 'bn', 'c8': 'bb', 'c3': 'bn', 'c2': 'wp', 'c1': 'wb', 'c7': 'bp', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': 'wb', 'f2': 'wp', 'f3': '  ', 'f4': '  ', 'f5': 'bp', 'f6': '  ', 'f7': '  ', 'f8': 'bb', 'b4': '  ', 'b5': '  ', 'b6': '  ', 'b7': 'bp', 'b1': 'wn', 'b2': 'wp', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': 'wp', 'a5': '  ', 'e8': 'bk', 'a7': 'bp', 'a6': '  ', 'e5': '  ', 'e4': 'wn', 'e7': 'bp', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': 'wp', 'a4': '  '})
#         self.assertEqual("""|br|  |bb|bq|bk|bb|bn|  |
# |bp|bp|bp|bp|bp|  |bp|wp|
# |  |  |  |  |  |  |  |  |
# |  |  |  |  |  |bp|wp|  |
# |  |  |  |  |wn|  |  |  |
# |  |  |bn|  |  |  |  |  |
# |wp|wp|wp|wp|wp|wp|  |  |
# |wr|wn|wb|wq|wk|wb|  |wr|
# """,self.zboard.show())

#     def test_expand_pawns_knights(self):
#         self.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': 'wp', 'h4': '  ', 'h5': '  ', 'd8': 'bq', 'a8': 'br', 'd6': '  ', 'd7': 'bp', 'd4': '  ', 'd5': '  ', 'd2': 'wp', 'd3': '  ', 'd1': 'wq', 'g7': 'bp', 'g6': '  ', 'g5': 'wp', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': 'bn', 'c8': 'bb', 'c3': 'bn', 'c2': 'wp', 'c1': 'wb', 'c7': 'bp', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': 'wb', 'f2': 'wp', 'f3': '  ', 'f4': '  ', 'f5': 'bp', 'f6': '  ', 'f7': '  ', 'f8': 'bb', 'b4': '  ', 'b5': '  ', 'b6': '  ', 'b7': 'bp', 'b1': 'wn', 'b2': 'wp', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': 'wp', 'a5': '  ', 'e8': 'bk', 'a7': 'bp', 'a6': '  ', 'e5': '  ', 'e4': 'wn', 'e7': 'bp', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': 'wp', 'a4': '  '})
#         #print(self.zboard.show())
#         #pawn capture right
#         self.assertEqual(set(['b4', 'b3', 'bxc3']),set([ x[2] for x in self.zboard.piece_by_sq('b2').expand(self.zboard.board)]))
#         #pawn capture right
#         self.assertEqual(set([('m','d4','d4'), ('m','d3','d3'), ('t','c3','dxc3')]),set(self.zboard.piece_by_sq('d2').expand(self.zboard.board)))
#         #blocked pawn
#         self.assertEqual([],self.zboard.piece_by_sq('c2').expand(self.zboard.board))
#         self.assertEqual([('m', 'e3', 'e3')],self.zboard.piece_by_sq('e2').expand(self.zboard.board))
#         #en passant without consideration of last move
#         self.assertEqual(set([('e', 'f6', 'gxf6'),('m', 'g6', 'g6')]),set(self.zboard.piece_by_sq('g5').expand(self.zboard.board)))
#         #promote pawn h7
#         self.assertEqual(set([('p', 'h8', 'h8R'),('p', 'h8', 'h8N'),('p', 'h8', 'h8B'),('p', 'h8', 'h8Q'),('+', 'g8', 'hxg8R'),('+', 'g8', 'hxg8N'),('+', 'g8', 'hxg8B'),('+', 'g8', 'hxg8Q')]),set(self.zboard.piece_by_sq('h7').expand(self.zboard.board)))

#         #knight at e4
#         self.assertEqual(set(['Nf6','Ng3','Nxc3','Nc5','Nd6']),set([ x[2] for x in self.zboard.piece_by_sq('e4').expand(self.zboard.board)]))
#         #knight at c3
#         self.assertEqual(set([('t', 'd1', 'Nxd1'),('t', 'a2', 'Nxa2'),('t', 'e2', 'Nxe2'),('m', 'b5', 'Nb5'),('m', 'a4', 'Na4'),('t', 'b1', 'Nxb1'),('m', 'd5', 'Nd5'),('t', 'e4', 'Nxe4')]),set(self.zboard.piece_by_sq('c3').expand(self.zboard.board)))

#     def test_add(self):
#         self.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': 'wp', 'h4': '  ', 'h5': '  ', 'd8': 'bq', 'a8': 'br', 'd6': '  ', 'd7': 'bp', 'd4': '  ', 'd5': '  ', 'd2': 'wp', 'd3': '  ', 'd1': 'wq', 'g7': 'bp', 'g6': '  ', 'g5': 'wp', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': 'bn', 'c8': 'bb', 'c3': 'bn', 'c2': 'wp', 'c1': 'wb', 'c7': 'bp', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': 'wb', 'f2': 'wp', 'f3': '  ', 'f4': '  ', 'f5': 'bp', 'f6': '  ', 'f7': '  ', 'f8': 'bb', 'b4': '  ', 'b5': '  ', 'b6': '  ', 'b7': 'bp', 'b1': 'wn', 'b2': 'wp', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': 'wp', 'a5': '  ', 'e8': 'bk', 'a7': 'bp', 'a6': '  ', 'e5': '  ', 'e4': 'wn', 'e7': 'bp', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': 'wp', 'a4': '  '})
#         for p in self.zboard.fullset():
#             if p.type == 'p':
#                 self.zboard.take(p)

#         self.zboard.add('w','b','b5')
#         self.zboard.add('bq@e5')
#         self.zboard.add('bb@d7')
#         self.zboard.add('wr@b7')
#         #self.zboard.boardify()
#         #print(self.zboard.board)
#         self.assertEqual('wb@b5',repr(self.zboard.piece_by_sq('b5')))
#         self.assertEqual('bq@e5',repr(self.zboard.piece_by_sq('e5')))
#         self.assertEqual('bb@d7',repr(self.zboard.piece_by_sq('d7')))
#         self.assertEqual('wr@b7',repr(self.zboard.piece_by_sq('b7')))

#     def test_expand_bishop_rook_queen_king(self):
#         self.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': '  ', 'h4': '  ', 'h5': '  ', 'd8': 'bq', 'a8': 'br', 'd6': '  ', 'd7': 'bb', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': 'wq', 'g7': '  ', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': 'bn', 'c8': 'bb', 'c3': 'bn', 'c2': '  ', 'c1': 'wb', 'c7': '  ', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': 'wb', 'f2': '  ', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': '  ', 'f8': 'bb', 'b4': '  ', 'b5': 'wb', 'b6': '  ', 'b7': 'wr', 'b1': 'wn', 'b2': '  ', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': '  ', 'a5': '  ', 'e8': 'bk', 'a7': '  ', 'a6': '  ', 'e5': 'bq', 'e4': 'wn', 'e7': '  ', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         #print('\n'+self.zboard.show())

#         """
#         |br|  |bb|bq|bk|bb|bn|  |
#         |  |wr|  |bb|  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |  |wb|  |  |bq|  |  |  |
#         |  |  |  |  |wn|  |  |  |
#         |  |  |bn|  |  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |wr|wn|wb|wq|wk|wb|  |wr|
#         """

#         #for sq in ['b5','c8','d7','c1','a8','b7','e5','d1','e8','e1']:
#         #    p = self.zboard.piece_by_sq(sq)
#         #    print(p,p.expand(self.zboard.board))

#         #white bishop at b5
#         self.assertEqual(set(['Ba4', 'Ba6', 'Bc6','Bxd7','Bc4','Bd3','Be2']),set([ x[2] for x in self.zboard.piece_by_sq('b5').expand(self.zboard.board)]))
#         #bishop at c8
#         self.assertEqual([('t','b7','Bxb7')],self.zboard.piece_by_sq('c8').expand(self.zboard.board))
#         #bishop at d7
#         self.assertEqual(set([('m', 'f5', 'Bf5'),('m', 'g4', 'Bg4'),('m', 'e6', 'Be6'),('t', 'b5', 'Bxb5'),('m', 'c6', 'Bc6'),('m', 'h3', 'Bh3')]),set(self.zboard.piece_by_sq('d7').expand(self.zboard.board)))
#         #bishop at c1
#         self.assertTrue(('m','e3','Be3') in self.zboard.piece_by_sq('c1').expand(self.zboard.board))

#         #rook at a8
#         self.assertEqual(set(['Rxa1', 'Ra2', 'Ra3','Ra4','Ra5','Ra6','Ra7','Rb8']),set([ x[2] for x in self.zboard.piece_by_sq('a8').expand(self.zboard.board)]))
#         #rook at b7
#         self.assertTrue(('t','d7','Rxd7') in self.zboard.piece_by_sq('b7').expand(self.zboard.board))

#         #print(self.zboard.piece_by_sq('h1').expand(self.zboard.board))

#         #queen at e5
#         self.assertEqual(set(['Qe7', 'Qe6', 'Qf6','Qg7','Qh8','Qf5', 'Qg5', 'Qh5','Qf4','Qg3','Qh2', 'Qxe4', 'Qd4','Qd5','Qc5','Qxb5', 'Qd6','Qc7','Qb8',]),set([ x[2] for x in self.zboard.piece_by_sq('e5').expand(self.zboard.board)]))
#         #queen at d1
#         self.assertTrue(('m','g4','Qg4') in self.zboard.piece_by_sq('d1').expand(self.zboard.board))

#         #king at e8
#         self.assertEqual(set([('m','e7','Ke7'),('m','f7','Kf7')]),set(self.zboard.piece_by_sq('e8').expand(self.zboard.board)))
#         #king at e1
#         self.assertTrue(('m','e2','Ke2') in self.zboard.piece_by_sq('e1').expand(self.zboard.board)) # no validation yet
#         #castling # no check validation yet
#         self.zboard.take(self.zboard.piece_by_sq('b1'))
#         self.zboard.take(self.zboard.piece_by_sq('c1'))
#         self.zboard.take(self.zboard.piece_by_sq('d1'))
#         self.zboard.take(self.zboard.piece_by_sq('f1'))
#         self.zboard.take(self.zboard.piece_by_sq('c8'))
#         self.zboard.take(self.zboard.piece_by_sq('d8'))
#         self.zboard.take(self.zboard.piece_by_sq('f8'))
#         self.zboard.take(self.zboard.piece_by_sq('g8'))
#         #print(self.zboard.board)
#         #print('\n'+self.zboard.show())
#         """
#         |br|  |  |  |bk|  |  |  |
#         |  |wr|  |bb|  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |  |wb|  |  |bq|  |  |  |
#         |  |  |  |  |wn|  |  |  |
#         |  |  |bn|  |  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |wr|  |  |  |wk|  |  |wr|
#         """
#         #king at e8
#         self.assertTrue(('c','c8','O-O-O') in self.zboard.piece_by_sq('e8').expand(self.zboard.board))
#         # O-O not expanded as per Rook missing from h8
#         #king at e1
#         self.assertTrue(('c','c1','O-O-O') in self.zboard.piece_by_sq('e1').expand(self.zboard.board))
#         self.assertTrue(('c','g1','O-O') in self.zboard.piece_by_sq('e1').expand(self.zboard.board))

#     def test_move_exceptions(self):
#         self.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': '  ', 'h4': '  ', 'h5': '  ', 'd8': 'bq', 'a8': 'br', 'd6': '  ', 'd7': 'bb', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': 'wq', 'g7': '  ', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': 'bn', 'c8': 'bb', 'c3': 'bn', 'c2': '  ', 'c1': 'wb', 'c7': '  ', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': 'wb', 'f2': '  ', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': '  ', 'f8': 'bb', 'b4': '  ', 'b5': 'wb', 'b6': '  ', 'b7': 'wr', 'b1': 'wn', 'b2': '  ', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': '  ', 'a5': '  ', 'e8': 'bk', 'a7': '  ', 'a6': '  ', 'e5': 'bq', 'e4': 'wn', 'e7': '  ', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         #print(self.zboard.piece_by_sq('c3'))
#         #self.zboard.relocate('c8','c3')
#         #self.zboard.relocate('b8','b6')
#         self.assertRaises(chesslib.MoveException, self.zboard.relocate,'c8','c3')
#         self.assertRaises(chesslib.MoveException, self.zboard.relocate,'b8','b6')

#     def test_incheck_checks(self):
#         self.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': '  ', 'h4': '  ', 'h5': '  ', 'd8': 'bq', 'a8': 'br', 'd6': '  ', 'd7': 'bb', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': 'wq', 'g7': '  ', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': 'bn', 'c8': 'bb', 'c3': 'bn', 'c2': '  ', 'c1': 'wb', 'c7': '  ', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': 'wb', 'f2': '  ', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': '  ', 'f8': 'bb', 'b4': '  ', 'b5': 'wb', 'b6': '  ', 'b7': 'wr', 'b1': 'wn', 'b2': '  ', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': '  ', 'a5': '  ', 'e8': 'bk', 'a7': '  ', 'a6': '  ', 'e5': 'bq', 'e4': '  ', 'e7': '  ', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         #print('\n'+self.zboard.show())
#         """
#         |br|  |bb|bq|bk|bb|bn|  |
#         |  |wr|  |bb|  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |  |wb|  |  |bq|  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |  |  |bn|  |  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |wr|wn|wb|wq|wk|wb|  |wr|
#         """

#         self.assertTrue(self.zboard.sq_in_check('e1','b'))
#         self.assertTrue(self.zboard.sq_in_check('e2','b'))
#         self.assertFalse(self.zboard.sq_in_check('f2','b'))
#         self.assertFalse(self.zboard.sq_in_check('d2','b'))
#         self.zboard.piecefy({'h8': 'br', 'h2': 'wp', 'h3': '  ', 'h1': 'wr', 'h6': 'bn', 'h7': 'bp', 'h4': '  ', 'h5': '  ', 'd8': 'bq', 'a8': 'br', 'd6': 'bp', 'd7': '  ', 'd4': '  ', 'd5': '  ', 'd2': 'wp', 'd3': '  ', 'd1': 'wq', 'g7': 'bp', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': 'wp', 'g1': 'wn', 'g8': '  ', 'c8': 'bb', 'c3': '  ', 'c2': 'wp', 'c1': 'wb', 'c7': 'bp', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': '  ', 'f2': 'wp', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': 'bp', 'f8': 'bb', 'b4': '  ', 'b5': 'wb', 'b6': '  ', 'b7': 'bp', 'b1': 'wn', 'b2': 'wp', 'b3': '  ', 'b8': 'bn', 'a1': 'wr', 'a3': '  ', 'a2': 'wp', 'a5': '  ', 'e8': 'bk', 'a7': 'bp', 'a6': '  ', 'e5': '  ', 'e4': 'wp', 'e7': 'bp', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         self.assertTrue(self.zboard.sq_in_check('e8','w'))

#         self.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': 'wp', 'h1': 'wr', 'h6': '  ', 'h7': 'bp', 'h4': '  ', 'h5': '  ', 'd8': 'bk', 'a8': 'br', 'd6': 'wp', 'd7': '  ', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': 'wr', 'g7': 'bq', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': 'wp', 'g2': 'wp', 'g1': '  ', 'g8': '  ', 'c8': 'bb', 'c3': 'wn', 'c2': 'wp', 'c1': 'wk', 'c7': '  ', 'c6': 'bp', 'c5': '  ', 'c4': '  ', 'f1': '  ', 'f2': '  ', 'f3': 'wq', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': 'wb', 'f8': '  ', 'b4': '  ', 'b5': '  ', 'b6': '  ', 'b7': 'bp', 'b1': '  ', 'b2': 'wp', 'b3': '  ', 'b8': 'bn', 'a1': '  ', 'a3': '  ', 'a2': 'wp', 'a5': '  ', 'e8': '  ', 'a7': 'bp', 'a6': '  ', 'e5': '  ', 'e4': '  ', 'e7': 'bp', 'e6': '  ', 'e1': '  ', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         #print '\n'+self.zboard.show()
#         #print self.zboard.valids(self.zboard.piece_by_sq('d8'))
#         self.assertFalse(('m', 'c7', 'Kc7')in self.zboard.valids(self.zboard.piece_by_sq('d8')))


#     def test_prevalidate_against_checks(self):
#         #note:since we dont have the the game class, we will use the _piecefy_ to reset the board back after executing every expansion for evaluation
#         self.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': '  ', 'h4': '  ', 'h5': '  ', 'd8': 'bq', 'a8': 'br', 'd6': '  ', 'd7': 'bb', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': 'wq', 'g7': '  ', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': 'bn', 'c8': 'bb', 'c3': 'bn', 'c2': '  ', 'c1': 'wb', 'c7': '  ', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': 'wb', 'f2': '  ', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': '  ', 'f8': 'bb', 'b4': '  ', 'b5': 'wb', 'b6': '  ', 'b7': 'wr', 'b1': 'wn', 'b2': '  ', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': '  ', 'a5': '  ', 'e8': 'bk', 'a7': '  ', 'a6': '  ', 'e5': 'bq', 'e4': 'wn', 'e7': '  ', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         #print('\n'+self.zboard.show())

#         """
#         |br|  |bb|bq|bk|bb|bn|  |
#         |  |wr|  |bb|  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |  |wb|  |  |bq|  |  |  |
#         |  |  |  |  |wn|  |  |  |
#         |  |  |bn|  |  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |wr|wn|wb|wq|wk|wb|  |wr|
#         """

#         resulting_expansions = {}
#         for p in self.zboard.fullset():
#             zkey = p.sq # original position of the pece we're working with denotes the key for the results

#             ### The segment below was outdated since the introduction of method board.validate_all_moves
#             ### The method board.validate_move, should be used to validate moves by the king, or in situations where there is already a king in check
#             if p.col == 'w':
#                 oposite_col = 'b'
#             else:
#                 oposite_col = 'w'
#             reductions = [] # list of the moves which will be excluded form the expansions, due to opening check
#             expansions = p.expand(self.zboard.board)
#             for e in expansions:
#                 #if p.sq=='e4':
#                 #    print(p,e,v)
#                 #    v = self.zboard.validate_move(p,e,1)
#                 #else:
#                 if p.type == 'k':
#                     v = self.zboard.prevalidate_all_moves(p,e)
#                 else:
#                     v = self.zboard.prevalidate_move(p,e)

#                 if not v:
#                     reductions.append(e)

#             resulting_expansions[zkey] = [x for x in expansions if x not in reductions]

#         # the knight at e4, will have the expansion list reduced to []
#         self.assertEqual([],resulting_expansions['e4'])
#         #bishop at d7 previously had [('m', 'f5', 'Bf5'),('m', 'g4', 'Bg4'),('m', 'e6', 'Be6'),('t', 'b5', 'Bxb5'),('m', 'c6', 'Bc6'),('m', 'h3', 'Bh3')], but now
#         self.assertEqual(set([('t', 'b5', 'Bxb5'),('m', 'c6', 'Bc6')]),set(resulting_expansions['d7']))
#         #king at e1 -- validated the move to e2 as it's hit by the knight at c3
#         self.assertFalse(('m','e2','Ke2') in resulting_expansions['e1'])

#         self.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': '  ', 'h4': '  ', 'h5': '  ', 'd8': '  ', 'a8': 'br', 'd6': '  ', 'd7': 'bb', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': '  ', 'g7': '  ', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': '  ', 'c8': '  ', 'c3': 'bn', 'c2': '  ', 'c1': '  ', 'c7': '  ', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': '  ', 'f2': '  ', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': '  ', 'f8': '  ', 'b4': '  ', 'b5': 'wb', 'b6': '  ', 'b7': 'wr', 'b1': '  ', 'b2': '  ', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': '  ', 'a5': '  ', 'e8': 'bk', 'a7': '  ', 'a6': '  ', 'e5': 'bq', 'e4': 'wn', 'e7': '  ', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         #print('\n'+self.zboard.show())
#         """
#         |br|  |  |  |bk|  |  |  |
#         |  |wr|  |bb|  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |  |wb|  |  |bq|  |  |  |
#         |  |  |  |  |wn|  |  |  |
#         |  |  |bn|  |  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |wr|  |  |  |wk|  |  |wr|
#         """
#         #king at e1 should not expand queen side castle dure to N@c3 hitting d1
#         reductions = [] # list of the moves which will be excluded form the expansions, due to opening check
#         expansions = self.zboard.piece_by_sq('e1').expand(self.zboard.board)
#         for e in expansions:
#             if not self.zboard.validate_all_moves(self.zboard.piece_by_sq('e1'),e): ## validate_all_moves because checking the king at e1
#                 reductions.append(e)
#         self.assertTrue(('c','c1','O-O-O') in reductions)


#     def test_valids_expansion(self):
#         self.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': '  ', 'h4': '  ', 'h5': '  ', 'd8': '  ', 'a8': 'br', 'd6': '  ', 'd7': 'bb', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': '  ', 'g7': '  ', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': '  ', 'c8': '  ', 'c3': 'bn', 'c2': '  ', 'c1': '  ', 'c7': '  ', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': '  ', 'f2': '  ', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': '  ', 'f8': '  ', 'b4': '  ', 'b5': 'wb', 'b6': '  ', 'b7': 'wr', 'b1': '  ', 'b2': '  ', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': '  ', 'a5': '  ', 'e8': 'bk', 'a7': '  ', 'a6': '  ', 'e5': 'bq', 'e4': 'wn', 'e7': '  ', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         #print('\n'+self.zboard.show())
#         """
#         |br|  |  |  |bk|  |  |  |
#         |  |wr|  |bb|  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |  |wb|  |  |bq|  |  |  |
#         |  |  |  |  |wn|  |  |  |
#         |  |  |bn|  |  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |wr|  |  |  |wk|  |  |wr|
#         """
#         #king at e1 should not expand queen side castle dure to N@c3 hitting d1
#         #king at e1 should not expand to e2 as it's hit by the N@c3
#         self.assertEqual(set([('m', 'd2', 'Kd2'),('m', 'f2', 'Kf2'),('m', 'f1', 'Kf1'),('c', 'g1', 'O-O')]),set(self.zboard.valids(self.zboard.piece_by_sq('e1'))))


#     def test_decode_move(self):
#         zgame = chesslib.game()
#         zgame.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': '  ', 'h4': '  ', 'h5': '  ', 'd8': '  ', 'a8': 'br', 'd6': '  ', 'd7': 'bb', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': '  ', 'g7': '  ', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': '  ', 'c8': '  ', 'c3': 'bn', 'c2': '  ', 'c1': '  ', 'c7': '  ', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': '  ', 'f2': '  ', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': '  ', 'f8': '  ', 'b4': '  ', 'b5': 'wb', 'b6': '  ', 'b7': 'wr', 'b1': '  ', 'b2': '  ', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': '  ', 'a5': '  ', 'e8': 'bk', 'a7': '  ', 'a6': '  ', 'e5': 'bq', 'e4': 'wn', 'e7': '  ', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         #print('\n'+zgame.zboard.show())
#         """
#         |br|  |  |  |bk|  |  |  |
#         |  |wr|  |bb|  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |  |wb|  |  |bq|  |  |  |
#         |  |  |  |  |wn|  |  |  |
#         |  |  |bn|  |  |  |  |  |
#         |  |  |  |  |  |  |  |  |
#         |wr|  |  |  |wk|  |  |wr|
#         """
#         self.assertEqual((zgame.zboard.piece_by_sq('e1'),'e1','m','f2','Kf2'),zgame.decode_move('13. Kf2',zgame.turnset()))
#         self.assertEqual((zgame.zboard.piece_by_sq('e1'),'e1','c','g1','O-O'),zgame.decode_move('O-O',zgame.turnset()))
#         # O-O-O because it only decodes against the set, without validation
#         self.assertEqual((zgame.zboard.piece_by_sq('e1'),'e1','c','c1','O-O-O'),zgame.decode_move('O-O-O',zgame.turnset()))
#         #print(zgame.show())
#         self.assertEqual((zgame.zboard.piece_by_sq('b5'),'b5','t','d7','Bxd7'),zgame.decode_move('Bxd7+',zgame.turnset()))
#         zgame.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': 'wp', 'h4': '  ', 'h5': '  ', 'd8': 'bq', 'a8': 'br', 'd6': '  ', 'd7': 'bp', 'd4': '  ', 'd5': '  ', 'd2': 'wp', 'd3': '  ', 'd1': 'wq', 'g7': 'bp', 'g6': '  ', 'g5': 'wp', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': 'bn', 'c8': 'bb', 'c3': 'bn', 'c2': 'wp', 'c1': 'wb', 'c7': 'bp', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': 'wb', 'f2': 'wp', 'f3': '  ', 'f4': '  ', 'f5': 'bp', 'f6': '  ', 'f7': '  ', 'f8': 'bb', 'b4': '  ', 'b5': '  ', 'b6': '  ', 'b7': 'bp', 'b1': 'wn', 'b2': 'wp', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': 'wp', 'a5': '  ', 'e8': 'bk', 'a7': 'bp', 'a6': '  ', 'e5': '  ', 'e4': 'wn', 'e7': 'bp', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': 'wp', 'a4': '  '})
#         """
#         |br|  |bb|bq|bk|bb|bn|  |
#         |bp|bp|bp|bp|bp|  |bp|wp|
#         |  |  |  |  |  |  |  |  |
#         |  |  |  |  |  |bp|wp|  |
#         |  |  |  |  |wn|  |  |  |
#         |  |  |bn|  |  |  |  |  |
#         |wp|wp|wp|wp|wp|wp|  |  |
#         |wr|wn|wb|wq|wk|wb|  |wr|
#         """
#         #print(zgame.show())
#         self.assertEqual((zgame.zboard.piece_by_sq('h7'),'h7','p','h8','h8Q'),zgame.decode_move('h8Q',zgame.turnset()))
#         self.assertEqual((zgame.zboard.piece_by_sq('h7'),'h7','+','g8','hxg8N'),zgame.decode_move('hxg8N',zgame.turnset()))
#         #print(zgame.decode_move('Rxh7',zgame.turnset())) # cant promote to King
#         self.assertRaises(chesslib.MoveException, zgame.decode_move, '999. b8',zgame.turnset())  # no pawn to reach b8
#         self.assertRaises(chesslib.MoveException, zgame.decode_move, '2 fxgdfgdfgsdfg',zgame.turnset())  # ##cannot take own
#         self.assertRaises(chesslib.MoveException, zgame.decode_move, 'Ra3',zgame.turnset())  # invalid

#         #e.p.
#         self.assertEqual((zgame.zboard.piece_by_sq('g5'),'g5','e','f6','gxf6'),zgame.decode_move('gxf6',zgame.turnset()))

#     def test_game_cycle_n_mate(self):
#         zgame = chesslib.game()
#         self.assertEqual('1-0',zgame.cycle(['1. e4','e5','2. Bc4','a6','3. Qf3','b5','Qxf7#'],0,verbose=0))
#         #print(zgame.full_notation)

#     def test_game_cycle_stalemate(self):
#         zgame = chesslib.game()
#         # Stalemate
#         zgame.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': '  ', 'h4': '  ', 'h5': '  ', 'd8': '  ', 'a8': 'br', 'd6': '  ', 'd7': 'bb', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': '  ', 'g7': '  ', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': '  ', 'c8': '  ', 'c3': 'bn', 'c2': '  ', 'c1': '  ', 'c7': '  ', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': '  ', 'f2': '  ', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': '  ', 'f8': '  ', 'b4': '  ', 'b5': 'wb', 'b6': '  ', 'b7': 'wr', 'b1': '  ', 'b2': '  ', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': '  ', 'a5': '  ', 'e8': 'bk', 'a7': '  ', 'a6': '  ', 'e5': 'bq', 'e4': 'wn', 'e7': '  ', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         self.assertEqual('1/2-1/2',zgame.cycle(['Bxd7','Kd8','Rh7','Ra2','Rxa2','Qa5','Rxa5','Ne2','Kxe2','exit'],0,verbose=0)) #stalemate

#         # Draws
#         zgame = chesslib.game()
#         zgame.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': '  ', 'h6': '  ', 'h7': '  ', 'h4': '  ', 'h5': '  ', 'd8': '  ', 'a8': '  ', 'd6': '  ', 'd7': '  ', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': '  ', 'g7': '  ', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': '  ', 'c8': '  ', 'c3': '  ', 'c2': '  ', 'c1': '  ', 'c7': '  ', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': '  ', 'f2': '  ', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': '  ', 'f8': '  ', 'b4': '  ', 'b5': '  ', 'b6': '  ', 'b7': '  ', 'b1': '  ', 'b2': '  ', 'b3': '  ', 'b8': '  ', 'a1': '  ', 'a3': '  ', 'a2': '  ', 'a5': '  ', 'e8': 'bk', 'a7': '  ', 'a6': '  ', 'e5': 'bq', 'e4': '  ', 'e7': '  ', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': 'wq', 'a4': '  '})
#         self.assertEqual('1/2-1/2',zgame.cycle(['Kd1','Qxe2','Kxe2','Ke7'],0,verbose=0))# draw -- should trigger on Kxe2
#         ### insert here test for King + light piece vs King draws ###

#         # Repetition Draw
#         zgame = chesslib.game()
#         zgame.zboard.piecefy({'h8': 'bk', 'h2': '  ', 'h3': '  ', 'h1': '  ', 'h6': '  ', 'h7': '  ', 'h4': '  ', 'h5': '  ', 'd8': '  ', 'a8': '  ', 'd6': '  ', 'd7': '  ', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': '  ', 'g7': '  ', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': '  ', 'c8': '  ', 'c3': '  ', 'c2': '  ', 'c1': '  ', 'c7': '  ', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': '  ', 'f2': '  ', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': '  ', 'f8': '  ', 'b4': '  ', 'b5': '  ', 'b6': '  ', 'b7': '  ', 'b1': '  ', 'b2': '  ', 'b3': '  ', 'b8': '  ', 'a1': '  ', 'a3': '  ', 'a2': '  ', 'a5': '  ', 'e8': '  ', 'a7': '  ', 'a6': '  ', 'e5': 'bq', 'e4': '  ', 'e7': '  ', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': 'wq', 'a4': '  '})
#         self.assertEqual('1/2-1/2',zgame.cycle(['Kd1','Qd5+','2.Qd2','Qh1+','Qe1','Qd5','4.Qd2','Qh1+','5.Qe1','Qh5+','Qe2','Qh1','Qe1','Qd5','exit'],0,verbose=0))# draw by repetition

#     def test_game_undo(self):
#         zgame = chesslib.game()
#         zgame.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': '  ', 'h4': '  ', 'h5': '  ', 'd8': '  ', 'a8': 'br', 'd6': '  ', 'd7': 'bb', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': '  ', 'g7': '  ', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': '  ', 'c8': '  ', 'c3': 'bn', 'c2': '  ', 'c1': '  ', 'c7': '  ', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': '  ', 'f2': '  ', 'f3': '  ', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': '  ', 'f8': '  ', 'b4': '  ', 'b5': 'wb', 'b6': '  ', 'b7': 'wr', 'b1': '  ', 'b2': '  ', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': '  ', 'a5': '  ', 'e8': 'bk', 'a7': '  ', 'a6': '  ', 'e5': 'bq', 'e4': 'wn', 'e7': '  ', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         #print(zgame.show())
#         zgame.cycle(['Bxd7','Kd8','Rh7','Ra2','Rxa2','Qa5','undo','exit'],0,verbose=0)
#         #zgame.turnundo()
#         #print(zgame.show())
#         self.assertEqual("""|  |  |  |bk|  |  |  |  |
# |  |wr|  |wb|  |  |  |wr|
# |  |  |  |  |  |  |  |  |
# |  |  |  |  |bq|  |  |  |
# |  |  |  |  |wn|  |  |  |
# |  |  |bn|  |  |  |  |  |
# |br|  |  |  |  |  |  |  |
# |wr|  |  |  |wk|  |  |  |
# """,zgame.zboard.show()) #before 'Rxa2' #by black

#     def test_game_cycle_ai(self):
#         zgame = chesslib.game(bplayer='ai',logfile='d:\\temp\\aigametest.txt') # using log different from the defailt, so that it doesn't get overwrittent by subsequent test
#         #cProfile.run('zgame.cycle(aidepth=4)')
#         #zgame.cycle(aidepth=2)

#     def test_ai_vs_ai(self):
#         #print
#         some_game = chesslib.game(wplayer='ai',bplayer='ai',logfile='d:\\temp\\aiaigametest.txt')
#         some_game.zboard.piecefy({'h8': '  ', 'h2': '  ', 'h3': 'wp', 'h1': 'wr', 'h6': '  ', 'h7': 'bp', 'h4': '  ', 'h5': '  ', 'd8': 'bk', 'a8': 'br', 'd6': 'bp', 'd7': '  ', 'd4': '  ', 'd5': '  ', 'd2': '  ', 'd3': '  ', 'd1': 'wr', 'g7': 'bq', 'g6': '  ', 'g5': '  ', 'g4': '  ', 'g3': 'wp', 'g2': 'wp', 'g1': '  ', 'g8': '  ', 'c8': 'bb', 'c3': 'wn', 'c2': 'wp', 'c1': 'wk', 'c7': '  ', 'c6': 'bp', 'c5': '  ', 'c4': '  ', 'f1': '  ', 'f2': '  ', 'f3': 'wq', 'f4': '  ', 'f5': '  ', 'f6': '  ', 'f7': 'wb', 'f8': '  ', 'b4': '  ', 'b5': '  ', 'b6': '  ', 'b7': 'bp', 'b1': '  ', 'b2': 'wp', 'b3': '  ', 'b8': 'bn', 'a1': '  ', 'a3': '  ', 'a2': 'wp', 'a5': '  ', 'e8': '  ', 'a7': 'bp', 'a6': '  ', 'e5': 'wp', 'e4': '  ', 'e7': 'bp', 'e6': '  ', 'e1': '  ', 'e3': '  ', 'e2': '  ', 'a4': '  '})
#         zgame = chesslib.game(wplayer='ai',bplayer='ai',logfile='d:\\temp\\aiaigametest.txt')
#         zgame.zboard = copy.deepcopy(some_game.zboard)
#         zgame.cycle(aidepth=2,verbose=0)
#         #print zgame.full_notation






