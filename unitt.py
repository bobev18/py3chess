import unittest

from piece import Piece
from move import Move, MoveException
from board import Board
from game import Game, Player, GameException


TEST_POSITION1 = {'h8':'  ', 'h2':'  ', 'h3':'  ', 'h1':'wr', 'h6':'  ', 'h7':'wp', 'h4':'  ', 'h5':'  ', 'd8':'bq', 'a8':'br', 'd6':'  ', 'd7':'bp', 'd4':'  ', 'd5':'  ', 'd2':'wp', 'd3':'  ', 'd1':'wq', 'g7':'bp', 'g6':'  ', 'g5':'wp', 'g4':'  ', 'g3':'  ', 'g2':'  ', 'g1':'  ', 'g8':'bn', 'c8':'bb', 'c3':'bn', 'c2':'wp', 'c1':'wb', 'c7':'bp', 'c6':'  ', 'c5':'  ', 'c4':'  ', 'f1':'wb', 'f2':'wp', 'f3':'  ', 'f4':'  ', 'f5':'bp', 'f6':'  ', 'f7':'  ', 'f8':'bb', 'b4':'  ', 'b5':'  ', 'b6':'  ', 'b7':'bp', 'b1':'wn', 'b2':'wp', 'b3':'  ', 'b8':'  ', 'a1':'wr', 'a3':'  ', 'a2':'wp', 'a5':'  ', 'e8':'bk', 'a7':'bp', 'a6':'  ', 'e5':'  ', 'e4':'wn', 'e7':'bp', 'e6':'  ', 'e1':'wk', 'e3':'  ', 'e2':'wp', 'a4':'  '}
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
TEST_POSITION2 = {'h8':'  ', 'h2':'  ', 'h3':'  ', 'h1':'wr', 'h6':'  ', 'h7':'  ', 'h4':'  ', 'h5':'  ', 'd8':'bq', 'a8':'br', 'd6':'  ', 'd7':'bb', 'd4':'  ', 'd5':'  ', 'd2':'  ', 'd3':'  ', 'd1':'wq', 'g7':'  ', 'g6':'  ', 'g5':'  ', 'g4':'  ', 'g3':'  ', 'g2':'  ', 'g1':'  ', 'g8':'bn', 'c8':'bb', 'c3':'bn', 'c2':'  ', 'c1':'wb', 'c7':'  ', 'c6':'  ', 'c5':'  ', 'c4':'  ', 'f1':'wb', 'f2':'  ', 'f3':'  ', 'f4':'  ', 'f5':'  ', 'f6':'  ', 'f7':'  ', 'f8':'bb', 'b4':'  ', 'b5':'wb', 'b6':'  ', 'b7':'wr', 'b1':'wn', 'b2':'  ', 'b3':'  ', 'b8':'  ', 'a1':'wr', 'a3':'  ', 'a2':'  ', 'a5':'  ', 'e8':'bk', 'a7':'  ', 'a6':'  ', 'e5':'bq', 'e4':'wn', 'e7':'  ', 'e6':'  ', 'e1':'wk', 'e3':'  ', 'e2':'  ', 'a4':'  '}
TEST_POSITION3 = {'h5':'  ', 'g2':'  ', 'f8':'  ', 'g5':'  ', 'd8':'  ', 'd4':'  ', 'c6':'  ', 'e2':'  ', 'b6':'  ', 'd3':'  ', 'b3':'  ', 'f1':'  ', 'a8':'br', 'a7':'  ', 'b1':'  ', 'f3':'  ', 'a6':'  ', 'a2':'  ', 'b2':'  ', 'h6':'  ', 'e3':'  ', 'f6':'  ', 'b7':'wr', 'd5':'  ', 'e4':'wn', 'd6':'  ', 'g7':'  ', 'e6':'  ', 'f2':'  ', 'g6':'  ', 'h7':'  ', 'c1':'  ', 'f4':'  ', 'd2':'  ', 'g1':'  ', 'a1':'wr', 'e8':'bk', 'c8':'  ', 'e5':'bq', 'e7':'  ', 'a4':'  ', 'h4':'  ', 'b5':'wb', 'c3':'bn', 'b4':'  ', 'g3':'  ', 'f7':'  ', 'c7':'  ', 'h1':'wr', 'h8':'  ', 'g8':'  ', 'a3':'  ', 'a5':'  ', 'f5':'  ', 'c4':'  ', 'e1':'wk', 'd7':'bb', 'g4':'  ', 'b8':'  ', 'h2':'  ', 'd1':'  ', 'h3':'  ', 'c5':'  ', 'c2':'  '}
TWO_KINGS_POSITION = {'h5':'  ', 'g2':'  ', 'f8':'  ', 'g5':'  ', 'd8':'  ', 'd4':'  ', 'c6':'  ', 'e2':'  ', 'b6':'  ', 'd3':'  ', 'b3':'  ', 'f1':'  ', 'a8':'  ', 'a7':'  ', 'b1':'  ', 'f3':'  ', 'a6':'  ', 'a2':'  ', 'b2':'  ', 'h6':'  ', 'e3':'  ', 'f6':'  ', 'b7':'  ', 'd5':'  ', 'e4':'  ', 'd6':'  ', 'g7':'  ', 'e6':'  ', 'f2':'  ', 'g6':'  ', 'h7':'  ', 'c1':'  ', 'f4':'  ', 'd2':'  ', 'g1':'  ', 'a1':'  ', 'e8':'  ', 'c8':'  ', 'e5':'wk', 'e7':'  ', 'a4':'  ', 'h4':'  ', 'b5':'  ', 'c3':'  ', 'b4':'  ', 'g3':'  ', 'f7':'  ', 'c7':'  ', 'h1':'  ', 'h8':'bk', 'g8':'  ', 'a3':'  ', 'a5':'  ', 'f5':'  ', 'c4':'  ', 'e1':'  ', 'd7':'  ', 'g4':'  ', 'b8':'  ', 'h2':'  ', 'd1':'  ', 'h3':'  ', 'c5':'  ', 'c2':'  '}

class PieceTest(unittest.TestCase):

    def test_piece_initialization(self):
        test_piece = Piece('w', 'p', 'e2')
        self.assertEqual('wp@e2',repr(test_piece))

    def test_lookup_moves_on_empty_board(self):
        another_piece = Piece('w', 'p', 'e2')
        self.assertEqual({'m': ['e3'], 't': ['d3', 'f3'], 'm2': ['e4']}, another_piece.lookup_moves())

        test_piece = Piece('w', 'p', 'e8')
        self.assertEqual({}, test_piece.lookup_moves())

class MoveTest(unittest.TestCase):

    def test_move_initialization(self):
        test_piece = Piece('w', 'p', 'e2')
        test_move = Move(test_piece, 'm2', 'e4', 'e4')
        self.assertEqual('e4', repr(test_move))

    def test_move_action_generation(self):
        test_piece = Piece('w', 'n', 'e4')
        taken_piece = Piece('b', 'n', 'c3')
        test_move = Move(test_piece, 't', 'c3', 'Nxc3', taken_piece)
        self.assertEqual('Nxc3', repr(test_move))
        self.assertEqual(taken_piece, test_move.taken)
        execution_actions, undo_actions = test_move.actions()
        self.assertEqual([{'act':'remove_piece', 'args':[taken_piece]}, {'act':'relocate_piece', 'args':[test_piece, 'c3']}], execution_actions)
        self.assertEqual([{'act':'relocate_piece', 'args':['c3', 'e4']}, {'act':'add_piece', 'args':[taken_piece]}], undo_actions)

    def test_enpassant_move_initialization(self):
        test_piece = Piece('w', 'p', 'g5')
        taken_piece = Piece('b', 'p', 'f5')
        enpasant_move = Move(test_piece, 'e', 'f6', 'gxf6', taken_piece)
        def attribute_lister(object_, attributes):
            return [ getattr(object_, z) for z in attributes ]

        move_attributes = ['piece', 'origin', 'type_', 'destination', 'notation', 'promote_to', 'taken', 'catsling_rook',]
        self.assertEqual([test_piece, 'g5', 'e', 'f6', 'gxf6', '', taken_piece, None], [enpasant_move.piece, enpasant_move.origin, enpasant_move.type_, enpasant_move.destination, enpasant_move.notation, enpasant_move.promote_to, enpasant_move.taken, enpasant_move.catsling_rook,])

class BoardTest(unittest.TestCase):

    def test_board_initialization(self):
        test_board = Board(TEST_POSITION1)
        self.assertEqual(POSITION1_VIEW,repr(test_board))
        self.assertIsInstance(test_board.state['e4'], Piece)
        self.assertEqual('wn@e4', repr(test_board.state['e4']))

    def test_piece_addition_to_board(self):
        test_board = Board()
        self.assertIsNone(test_board.state['e4'])
        test_board.add_piece('w', 'n', 'e4')
        self.assertIsInstance(test_board.state['e4'], Piece)
        self.assertEqual('wn@e4', repr(test_board.state['e4']))

        self.assertIsNone(test_board.state['c3'])
        test_board.add_piece('bn@c3')
        self.assertEqual('bn@c3', repr(test_board.state['c3']))

        new_piece = Piece('w', 'n', 'b1')
        self.assertIsNone(test_board.state['b1'])
        test_board.add_piece(new_piece)
        self.assertEqual('wn@b1', repr(test_board.state['b1']))

    def test_piece_removal_from_board(self):
        test_board = Board(TEST_POSITION1)
        self.assertEqual('wn@e4', repr(test_board.state['e4']))
        test_board.remove_piece('e4')
        self.assertIsNone(test_board.state['e4'])

    def test_piece_relocation(self):
        test_board = Board(TEST_POSITION1)
        self.assertIsNone(test_board.state['b8'])
        test_board.relocate_piece('c3', 'b8')
        self.assertEqual('bn@b8', repr(test_board.state['b8']))
        test_board.relocate_piece('e4', 'g1')
        self.assertEqual('wn@g1', repr(test_board.state['g1']))
        test_board.relocate_piece('g5', 'g2')
        self.assertEqual('wp@g2', repr(test_board.state['g2']))
        test_board.relocate_piece(test_board.state['f5'], 'f7')
        self.assertEqual('bp@f7', repr(test_board.state['f7']))

        test_board = Board(TEST_POSITION2)
        self.assertRaises(MoveException, test_board.relocate_piece, 'c8', 'c3')
        self.assertRaises(MoveException, test_board.relocate_piece, 'b8', 'b6')

    def test_naive_moves_for_pawns_knights(self):
        test_board = Board(TEST_POSITION1)
        # |br|  |bb|bq|bk|bb|bn|  |
        # |bp|bp|bp|bp|bp|  |bp|wp|
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |  |bp|wp|  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |wp|wp|wp|wp|wp|wp|  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|

        #pawn capture right
        b2_moves = test_board.naive_moves(test_board.state['b2'])
        for move in b2_moves:
            self.assertIsInstance(move, Move)
        self.assertEqual(set(['b3', 'b4', 'bxc3']), set([ z.notation for z in b2_moves ]))
        #pawn capture left
        self.assertEqual(set(['d4', 'd3', 'dxc3']), set([ z.notation for z in test_board.naive_moves(test_board.state['d2']) ]))
        #blocked pawn
        self.assertEqual([], test_board.naive_moves(test_board.state['c2']))
        e2_moves = test_board.naive_moves(test_board.state['e2'])
        self.assertEqual(1, len(e2_moves))
        e2_move = e2_moves[0]
        self.assertEqual('e3', e2_move.notation)
        #en passant without consideration of last move
        self.assertIn('gxf6', [ z.notation for z in test_board.naive_moves(test_board.state['g5']) ])
        #promote pawn h7
        self.assertEqual(set(['h8R', 'h8N', 'h8B', 'h8Q', 'hxg8R', 'hxg8N', 'hxg8B', 'hxg8Q']), set([ z.notation for z in test_board.naive_moves(test_board.state['h7']) ]))

        #knight at e4
        self.assertEqual(set(['Nf6', 'Ng3', 'Nxc3', 'Nc5', 'Nd6']), set([ z.notation for z in test_board.naive_moves(test_board.state['e4'])]))
        #knight at c3
        self.assertEqual(set(['Nxd1', 'Nxa2', 'Nxe2', 'Nb5', 'Na4', 'Nxb1', 'Nd5', 'Nxe4']), set([ z.notation for z in test_board.naive_moves(test_board.state['c3']) ]))

    def test_naive_moves_for_bishops(self):
        test_board = Board(TEST_POSITION2)
        # |br|  |bb|bq|bk|bb|bn|  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|

        #white bishop at b5
        self.assertEqual(set(['Ba4', 'Ba6', 'Bc6', 'Bxd7', 'Bc4', 'Bd3', 'Be2']), set([ z.notation for z in test_board.naive_moves(test_board.state['b5']) ]))
        #bishop at c8
        Bc8_moves = test_board.naive_moves(test_board.state['c8'])
        self.assertEqual(1, len(Bc8_moves))
        self.assertEqual(['t', 'c8', 'b7', 'Bxb7'], [Bc8_moves[0].type_, Bc8_moves[0].origin, Bc8_moves[0].destination, Bc8_moves[0].notation])

        #bishop at d7
        self.assertEqual(set(['Bf5', 'Bg4', 'Be6', 'Bxb5', 'Bc6', 'Bh3']), set([ z.notation for z in test_board.naive_moves(test_board.state['d7']) ]))
        #bishop at c1
        self.assertIn('Be3', [ z.notation for z in test_board.naive_moves(test_board.state['c1']) ])

    def test_naive_moves_for_rooks(self):
        test_board = Board(TEST_POSITION2)
        # |br|  |bb|bq|bk|bb|bn|  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|
        #rook at a8
        self.assertEqual(set(['Rxa1', 'Ra2', 'Ra3', 'Ra4', 'Ra5', 'Ra6', 'Ra7', 'Rb8']), set([ z.notation for z in test_board.naive_moves(test_board.state['a8']) ]))
        #rook at b7
        self.assertIn('Rxd7', [ z.notation for z in test_board.naive_moves(test_board.state['b7']) ])

    def test_naive_moves_for_queens(self):
        test_board = Board(TEST_POSITION2)
        # |br|  |bb|bq|bk|bb|bn|  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|

        #queen at e5
        self.assertEqual(set(['Qe7', 'Qe6', 'Qf6', 'Qg7', 'Qh8', 'Qf5', 'Qg5', 'Qh5', 'Qf4', 'Qg3', 'Qh2', 'Qxe4', 'Qd4', 'Qd5', 'Qc5', 'Qxb5', 'Qd6', 'Qc7', 'Qb8',]),
            set([ z.notation for z in test_board.naive_moves(test_board.state['e5']) ]))
        #queen at d1
        self.assertIn('Qg4', [ z.notation for z in test_board.naive_moves(test_board.state['d1']) ])

    def test_naive_moves_for_kings(self):
        test_board = Board(TEST_POSITION2)
        # |br|  |bb|bq|bk|bb|bn|  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|

        #king at e8
        self.assertEqual(2, len(test_board.naive_moves(test_board.state['e8'])))
        self.assertIn('Ke7', [ z.notation for z in test_board.naive_moves(test_board.state['e8']) ])
        self.assertIn('Kf7', [ z.notation for z in test_board.naive_moves(test_board.state['e8']) ])
        #king at e1
        self.assertIn('Ke2', [ z.notation for z in test_board.naive_moves(test_board.state['e1']) ])

        #castling without check validation
        self.assertNotIn('O-O-O', [ z.notation for z in test_board.naive_moves(test_board.state['e8']) ])
        test_board = Board(TEST_POSITION3)
        # |br|  |  |  |bk|  |  |  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|  |  |  |wk|  |  |wr|
        #king at e8
        self.assertIn('O-O-O', [ z.notation for z in test_board.naive_moves(test_board.state['e8']) ])
        self.assertNotIn('O-O', [ z.notation for z in test_board.naive_moves(test_board.state['e8']) ])

        #king at e1
        self.assertIn('O-O', [ z.notation for z in test_board.naive_moves(test_board.state['e1']) ])
        self.assertIn('O-O-O', [ z.notation for z in test_board.naive_moves(test_board.state['e1']) ])

    def test_determining_checks(self):
        test_board = Board(TEST_POSITION2)
        self.assertFalse(test_board.discover_check('e8', 'd7', 'w'))
        self.assertFalse(test_board.discover_check('e1', 'e4', 'b'))
        test_board.remove_piece('e4')
        self.assertTrue(test_board.discover_check('e1', 'e4', 'b'))
        # |br|  |  |  |bk|  |  |  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|  |  |  |wk|  |  |wr|

        self.assertTrue(test_board.is_in_check('e1','b'))
        self.assertTrue(test_board.is_in_check('e2','b'))
        self.assertFalse(test_board.is_in_check('f2','b'))
        self.assertFalse(test_board.is_in_check('d2','b'))
        self.assertTrue(test_board.is_in_check('h8','w'))

    def test_execute_move(self):
        test_board = Board(TEST_POSITION1)
        # |br|  |bb|bq|bk|bb|bn|  |
        # |bp|bp|bp|bp|bp|  |bp|wp|
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |  |bp|wp|  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |wp|wp|wp|wp|wp|wp|  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|

        b1_moves = test_board.naive_moves(test_board.state['b1'])
        capture_move = [ z for z in b1_moves if z.type_ == 't' ][0]
        self.assertIsInstance(test_board.state['c3'], Piece)
        self.assertEqual('bn@c3', repr(test_board.state['c3']))
        self.assertEqual(14, len(test_board.black))
        undo = test_board.execute_move(capture_move)
        self.assertIsNotNone(undo)
        self.assertIsInstance(test_board.state['c3'], Piece)
        self.assertEqual('wn@c3', repr(test_board.state['c3']))
        self.assertEqual(13, len(test_board.black))

        test_board = Board(TEST_POSITION2)
        # |br|  |  |  |bk|  |  |  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|  |  |  |wk|  |  |wr|

        e4_moves = test_board.naive_moves(test_board.state['e4'])
        capture_move = [ z for z in e4_moves if z.type_ == 't' ][0]
        self.assertIsInstance(test_board.state['c3'], Piece)
        self.assertEqual('bn@c3', repr(test_board.state['c3']))
        undo = test_board.execute_move(capture_move)
        # move fails
        self.assertIsNone(undo)
        self.assertEqual('bn@c3', repr(test_board.state['c3']))
        self.assertEqual('wn@e4', repr(test_board.state['e4']))

    def test_undo_move(self):
        test_board = Board(TEST_POSITION1)
        # |br|  |bb|bq|bk|bb|bn|  |
        # |bp|bp|bp|bp|bp|  |bp|wp|
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |  |bp|wp|  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |wp|wp|wp|wp|wp|wp|  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|

        b1_moves = test_board.naive_moves(test_board.state['b1'])
        capture_move = [ z for z in b1_moves if z.type_ == 't' ][0]
        self.assertIsInstance(test_board.state['c3'], Piece)
        self.assertEqual('bn@c3', repr(test_board.state['c3']))
        self.assertEqual(16, len(test_board.white))
        self.assertEqual(14, len(test_board.black))
        undo = test_board.execute_move(capture_move)
        self.assertIsNotNone(undo)
        self.assertIsInstance(test_board.state['c3'], Piece)
        self.assertEqual('wn@c3', repr(test_board.state['c3']))
        self.assertEqual(16, len(test_board.white))
        self.assertEqual(13, len(test_board.black))
        test_board.undo_actions(undo)
        self.assertIsInstance(test_board.state['c3'], Piece)
        self.assertEqual('bn@c3', repr(test_board.state['c3']))
        self.assertEqual(16, len(test_board.white))
        self.assertEqual(14, len(test_board.black))

class GameTest(unittest.TestCase):

    def test_initialize_game(self):
        test_game = Game()
        self.assertEqual('wk@e1', repr(test_game.board.state['e1']))
        self.assertEqual(16, len(test_game.board.black))

    def test_validions_against_checks(self):
        test_game = Game(board_position=TEST_POSITION2)
        # |br|  |bb|bq|bk|bb|bn|  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|

        # the knight at e4, will have the expansion list reduced to []
        self.assertEqual([], test_game.valid_moves_of_piece_at('e4'))
        #bishop at d7 previously had [('m', 'f5', 'Bf5'),('m', 'g4', 'Bg4'),('m', 'e6', 'Be6'),('t', 'b5', 'Bxb5'),('m', 'c6', 'Bc6'),('m', 'h3', 'Bh3')], but now
        self.assertEqual(set(['Bxb5', 'Bc6']), set([ z.notation for z in test_game.valid_moves_of_piece_at('d7') ]))
        #king at e1 -- validated the move to e2 as it's hit by the knight at c3
        self.assertNotIn('Ke2', [ z.notation for z in test_game.valid_moves_of_piece_at('e1') ])

        test_game = Game(board_position=TEST_POSITION3)
        # |br|  |  |  |bk|  |  |  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|  |  |  |wk|  |  |wr|

        #king at e1 should not expand queen side castle due to N@c3 hitting d1
        naive_moves = set([ z.notation for z in test_game.board.naive_moves(test_game.board.state['e1']) ])
        valid_moves = set([ z.notation for z in test_game.valid_moves_of_piece_at('e1') ])
        self.assertTrue(set(['O-O-O']), naive_moves - valid_moves)

        self.assertEqual(set(['Kd2', 'Kf2', 'Kf1', 'O-O']), set([ z.notation for z in test_game.valid_moves_of_piece_at('e1') ]))

    def test_validations_of_covering_moves(self):
        test_game = Game(board_position=TEST_POSITION3)
        test_game.board.remove_piece('e4')
        # |br|  |  |  |bk|  |  |  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|  |  |  |wk|  |  |wr|
        test_game.board.white_checked = True

        whites_possible_moves = []
        for piece in test_game.board.pieces_of_color('w'):
            temporary_result = test_game.valid_moves_of_piece_at(piece.location)
            whites_possible_moves.extend(temporary_result)

        self.assertEqual(set(['Kd2', 'Kf2', 'Kf1', 'Be2']), set([ z.notation for z in whites_possible_moves ]))

    def test_decode_move(self):
        test_game = Game(board_position=TEST_POSITION3)
        # |br|  |  |  |bk|  |  |  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|  |  |  |wk|  |  |wr|
        king = test_game.board.state['e1']
        a_rook = test_game.board.state['a1']
        h_rook = test_game.board.state['h1']
        king_side_castle = Move(king,'c', 'g1', 'O-O', h_rook)
        decoded_move = test_game.decode_move('O-O', test_game.board.white)
        # print(king_side_castle, [ getattr(king_side_castle, z) for z in ['piece', 'origin', 'type_', 'destination', 'notation', 'promote_to', 'taken', 'catsling_rook',] ])
        # print(decoded_move, [ getattr(decoded_move, z) for z in ['piece', 'origin', 'type_', 'destination', 'notation', 'promote_to', 'taken', 'catsling_rook',] ])

        def attribute_lister(object_, attributes):
            return [ getattr(object_, z) for z in attributes ]

        move_attributes = ['piece', 'origin', 'type_', 'destination', 'notation', 'promote_to', 'taken', 'catsling_rook',]

        self.assertEqual(attribute_lister(king_side_castle, move_attributes) , attribute_lister(decoded_move, move_attributes))
        # O-O-O because it only decodes against the set, without validation
        queen_side_castle = Move(king,'c', 'c1', 'O-O-O', a_rook)
        decoded_move = test_game.decode_move('O[O]O', test_game.board.white)
        self.assertEqual(attribute_lister(queen_side_castle, move_attributes) , attribute_lister(decoded_move, move_attributes))
        decoded_move = test_game.decode_move('OOO', test_game.board.white)
        self.assertEqual(attribute_lister(queen_side_castle, move_attributes) , attribute_lister(decoded_move, move_attributes))
        decoded_move = test_game.decode_move('O,>oOo-0*O', test_game.board.white)                                                                     #TOFIX?
        # print(attribute_lister(queen_side_castle, move_attributes))
        # print(attribute_lister(decoded_move, move_attributes))
        self.assertEqual(attribute_lister(queen_side_castle, move_attributes) , attribute_lister(decoded_move, move_attributes))
        # The above is left as reminder to rethink the decoding at some point

        #print(zgame.show())
        expected_move = Move(king, 'm', 'f2', 'Kf2')
        decoded_move = test_game.decode_move('13. Kf2', test_game.board.white)
        self.assertEqual(attribute_lister(expected_move, move_attributes) , attribute_lister(decoded_move, move_attributes))
        # self.assertEqual((zgame.zboard.piece_by_sq('e1'),'e1', 'm', 'f2', 'Kf2'), test_player.decode_move('13. Kf2', zgame.turnset()))
        expected_move = Move(test_game.board.state['b5'], 't', 'd7', 'Bxd7', test_game.board.state['d7'])
        decoded_move = test_game.decode_move('Bxd7+', test_game.board.white)
        self.assertEqual(attribute_lister(expected_move, move_attributes) , attribute_lister(decoded_move, move_attributes))

        test_game = Game(board_position=TEST_POSITION1)
        # |br|  |bb|bq|bk|bb|bn|  |
        # |bp|bp|bp|bp|bp|  |bp|wp|
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |  |bp|wp|  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |wp|wp|wp|wp|wp|wp|  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|

        no_promo_move_attributes = ['piece', 'origin', 'type_', 'destination', 'notation', 'taken', 'catsling_rook',]
        new_black_queen = Piece('b', 'q', 'h8')
        expected_move = Move(test_game.board.state['h7'], 'p', 'h8', 'h8Q', new_black_queen)
        decoded_move = test_game.decode_move('h8Q', test_game.board.white)
        self.assertEqual(attribute_lister(expected_move, no_promo_move_attributes) , attribute_lister(decoded_move, no_promo_move_attributes))

        new_black_knight = Piece('b', 'n', 'g8')
        expected_move = Move(test_game.board.state['h7'], '+', 'g8', 'hxg8N', [new_black_knight, test_game.board.state['g8']])
        decoded_move = test_game.decode_move('hxg8N', test_game.board.white)
        self.assertEqual(attribute_lister(expected_move, no_promo_move_attributes) , attribute_lister(decoded_move, no_promo_move_attributes))
        # assertRaises(exc, fun, *args, **kwds)
        self.assertRaises(MoveException, test_game.decode_move, '999. b8', test_game.board.white)  # no pawn to reach b8
        self.assertRaises(MoveException, test_game.decode_move, '2 fxgdfgdfgsdfg', test_game.board.white)  ### destination not on board
        self.assertRaises(MoveException, test_game.decode_move, 'Ra3', test_game.board.white)  # invalid
        # #e.p.
        expected_move = Move(test_game.board.state['g5'], 'e', 'f6', 'gxf6', test_game.board.state['f5'])
        decoded_move = test_game.decode_move('gxf6', test_game.board.white)
        self.assertEqual(attribute_lister(expected_move, move_attributes) , attribute_lister(decoded_move, move_attributes))

    def test_start_n_end_game(self):
        test_game = Game(board_position=TWO_KINGS_POSITION)
        self.assertEqual('stalemate', test_game.start(verbose=False))

    def test_game_cycle_mate(self):
        test_game = Game()
        test_game.whites_player.simulate( ['1. e4', '2. Bc4', '3. Qf3', 'Qxf7#'])
        test_game.blacks_player.simulate( [ 'e5',  'a6',  'b5', ])
        self.assertEqual('mate', test_game.start(verbose=False))

    def test_game_cycle_stalemate(self):
        position = {'h8':'  ', 'h2':'  ', 'h3':'  ', 'h1':'wr', 'h6':'  ', 'h7':'  ', 'h4':'  ', 'h5':'  ', 'd8':'  ', 'a8':'br', 'd6':'  ', 'd7':'bb', 'd4':'  ', 'd5':'  ', 'd2':'  ', 'd3':'  ', 'd1':'  ', 'g7':'  ', 'g6':'  ', 'g5':'  ', 'g4':'  ', 'g3':'  ', 'g2':'  ', 'g1':'  ', 'g8':'  ', 'c8':'  ', 'c3':'bn', 'c2':'  ', 'c1':'  ', 'c7':'  ', 'c6':'  ', 'c5':'  ', 'c4':'  ', 'f1':'  ', 'f2':'  ', 'f3':'  ', 'f4':'  ', 'f5':'  ', 'f6':'  ', 'f7':'  ', 'f8':'  ', 'b4':'  ', 'b5':'wb', 'b6':'  ', 'b7':'wr', 'b1':'  ', 'b2':'  ', 'b3':'  ', 'b8':'  ', 'a1':'wr', 'a3':'  ', 'a2':'  ', 'a5':'  ', 'e8':'bk', 'a7':'  ', 'a6':'  ', 'e5':'bq', 'e4':'wn', 'e7':'  ', 'e6':'  ', 'e1':'wk', 'e3':'  ', 'e2':'  ', 'a4':'  '}
        test_game = Game(board_position=position)
        # |br|  |  |  |bk|  |  |  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|  |  |  |wk|  |  |wr|
        test_game.whites_player.simulate(['Bxd7', 'Rh7', 'Rxa2', 'Rxa5', 'Kxe2', 'exit'])
        test_game.blacks_player.simulate(['Kd8', 'Ra2', 'Qa5', 'Ne2', ])
        self.assertEqual('stalemate', test_game.start(verbose=False))

    def test_game_cycle_draw(self):
        position = {'h8':'  ', 'h2':'  ', 'h3':'  ', 'h1':'  ', 'h6':'  ', 'h7':'  ', 'h4':'  ', 'h5':'  ', 'd8':'  ', 'a8':'  ', 'd6':'  ', 'd7':'  ', 'd4':'  ', 'd5':'  ', 'd2':'  ', 'd3':'  ', 'd1':'  ', 'g7':'  ', 'g6':'  ', 'g5':'  ', 'g4':'  ', 'g3':'  ', 'g2':'  ', 'g1':'  ', 'g8':'  ', 'c8':'  ', 'c3':'  ', 'c2':'  ', 'c1':'  ', 'c7':'  ', 'c6':'  ', 'c5':'  ', 'c4':'  ', 'f1':'  ', 'f2':'  ', 'f3':'  ', 'f4':'  ', 'f5':'  ', 'f6':'  ', 'f7':'  ', 'f8':'  ', 'b4':'  ', 'b5':'  ', 'b6':'  ', 'b7':'  ', 'b1':'  ', 'b2':'  ', 'b3':'  ', 'b8':'  ', 'a1':'  ', 'a3':'  ', 'a2':'  ', 'a5':'  ', 'e8':'bk', 'a7':'  ', 'a6':'  ', 'e5':'bq', 'e4':'  ', 'e7':'  ', 'e6':'  ', 'e1':'wk', 'e3':'  ', 'e2':'wq', 'a4':'  '}
        test_game = Game(board_position=position)
        # |  |  |  |  |bk|  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |bq|  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |wq|  |  |  |
        # |  |  |  |  |wk|  |  |  |
        test_game.whites_player.simulate(['Kd1', 'Kxe2'])
        test_game.blacks_player.simulate(['Qxe2', 'Ke7'])
        self.assertEqual('stalemate', test_game.start(verbose=False))

    def test_game_cycle_repetition_draw(self):
        position = {'h8':'bk', 'h2':'  ', 'h3':'  ', 'h1':'  ', 'h6':'  ', 'h7':'  ', 'h4':'  ', 'h5':'  ', 'd8':'  ', 'a8':'  ', 'd6':'  ', 'd7':'  ', 'd4':'  ', 'd5':'  ', 'd2':'  ', 'd3':'  ', 'd1':'  ', 'g7':'  ', 'g6':'  ', 'g5':'  ', 'g4':'  ', 'g3':'  ', 'g2':'  ', 'g1':'  ', 'g8':'  ', 'c8':'  ', 'c3':'  ', 'c2':'  ', 'c1':'  ', 'c7':'  ', 'c6':'  ', 'c5':'  ', 'c4':'  ', 'f1':'  ', 'f2':'  ', 'f3':'  ', 'f4':'  ', 'f5':'  ', 'f6':'  ', 'f7':'  ', 'f8':'  ', 'b4':'  ', 'b5':'  ', 'b6':'  ', 'b7':'  ', 'b1':'  ', 'b2':'  ', 'b3':'  ', 'b8':'  ', 'a1':'  ', 'a3':'  ', 'a2':'  ', 'a5':'  ', 'e8':'  ', 'a7':'  ', 'a6':'  ', 'e5':'bq', 'e4':'  ', 'e7':'  ', 'e6':'  ', 'e1':'wk', 'e3':'  ', 'e2':'wq', 'a4':'  '}
        test_game = Game(board_position=position)
        # |  |  |  |  |  |  |  |bk|
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |bq|  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |wq|  |  |  |
        # |  |  |  |  |wk|  |  |  |
        test_game.whites_player.simulate(['Kd1', '2.Qd2', 'Qe1', '4.Qd2', '5.Qe1', 'Qe2', 'Qe1', 'exit'])
        test_game.blacks_player.simulate(['Qd5+', 'Qh1+', 'Qd5', 'Qh1+', 'Qh5+', 'Qh1', 'Qd5', 'exit'])
        self.assertEqual('stalemate', test_game.start(verbose=False))


    def test_validations_of_enpassant_move_against_history(self):
        test_game = Game()
        test_game.whites_player.simulate(['e4', 'Nf3', 'Bc4', 'b4', 'Kf1', 'Ke1', 'O-O'])
        test_game.blacks_player.simulate(['a5', 'a4', 'Nc6', 'h6', 'axb3', 'h5', 'bxa2', ])
        self.assertRaises(GameException, test_game.start, False)

    def test_validations_of_castling_move_against_history(self):
        test_game = Game()
        test_game.whites_player.simulate(['e4', 'Nf3', 'Bc4', 'b4', 'Kf1', 'Ke1', 'O-O', 'Nc3'])
        test_game.blacks_player.simulate(['a5', 'a4', 'Nc6', 'axb3', 'h6', 'bxa2', 'h5'])
        self.assertRaises(GameException, test_game.start, False)


class TemporaryGameTest(unittest.TestCase):
    pass

#     def test_game_cycle_ai(self):
#         zgame = chesslib.game(bplayer='ai',logfile='d:\\temp\\aigametest.txt') # using log different from the defailt, so that it doesn't get overwrittent by subsequent test
#         #cProfile.run('zgame.cycle(aidepth=4)')
#         #zgame.cycle(aidepth=2)

#     def test_ai_vs_ai(self):
#         #print
#         some_game = chesslib.game(wplayer='ai',bplayer='ai',logfile='d:\\temp\\aiaigametest.txt')
#         some_game.zboard.piecefy({'h8':'  ', 'h2':'  ', 'h3':'wp', 'h1':'wr', 'h6':'  ', 'h7':'bp', 'h4':'  ', 'h5':'  ', 'd8':'bk', 'a8':'br', 'd6':'bp', 'd7':'  ', 'd4':'  ', 'd5':'  ', 'd2':'  ', 'd3':'  ', 'd1':'wr', 'g7':'bq', 'g6':'  ', 'g5':'  ', 'g4':'  ', 'g3':'wp', 'g2':'wp', 'g1':'  ', 'g8':'  ', 'c8':'bb', 'c3':'wn', 'c2':'wp', 'c1':'wk', 'c7':'  ', 'c6':'bp', 'c5':'  ', 'c4':'  ', 'f1':'  ', 'f2':'  ', 'f3':'wq', 'f4':'  ', 'f5':'  ', 'f6':'  ', 'f7':'wb', 'f8':'  ', 'b4':'  ', 'b5':'  ', 'b6':'  ', 'b7':'bp', 'b1':'  ', 'b2':'wp', 'b3':'  ', 'b8':'bn', 'a1':'  ', 'a3':'  ', 'a2':'wp', 'a5':'  ', 'e8':'  ', 'a7':'bp', 'a6':'  ', 'e5':'wp', 'e4':'  ', 'e7':'bp', 'e6':'  ', 'e1':'  ', 'e3':'  ', 'e2':'  ', 'a4':'  '})
#         zgame = chesslib.game(wplayer='ai',bplayer='ai',logfile='d:\\temp\\aiaigametest.txt')
#         zgame.zboard = copy.deepcopy(some_game.zboard)
#         zgame.cycle(aidepth=2,verbose=0)
#         #print zgame.full_notation


if __name__ == "__main__":
    try: unittest.main()
    except SystemExit: pass













