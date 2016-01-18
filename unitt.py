import unittest

from piece import Piece
from move import Move
from board import Board, MoveException
from game import Game, SimulationException
from player import Player, MoveExhaustException, DecodeException


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
        self.assertEqual({'m': ['e3'], 't': ['d3', 'f3'], 'm2': ['e4']}, another_piece.raw_moves)

        test_piece = Piece('w', 'p', 'e8')
        self.assertEqual({}, test_piece.raw_moves)

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
        self.assertEqual([('remove_piece', [taken_piece]), ('relocate_piece', [test_piece, 'c3'])], execution_actions)
        self.assertEqual([('relocate_piece', ['c3', 'e4']), ('add_piece', [taken_piece])], undo_actions)

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
        # because `.remove_piece('e4')` is called directly, `.process_ctions` is never called to gen the heat map (same with initial spawn)
        test_board.recapture_heat('b')

        self.assertTrue(test_board.discover_check('e1', 'e4', 'b'))
        # |br|  |bb|bq|bk|bb|bn|  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|

        self.assertTrue(test_board.is_in_check('e1','b'))
        self.assertTrue(test_board.is_in_check('e2','b'))
        self.assertFalse(test_board.is_in_check('f2','b'))
        self.assertFalse(test_board.is_in_check('d2','b'))
        test_board.recapture_heat('w')
        self.assertTrue(test_board.is_in_check('h8','w'))

    def test_find_checkers(self):
        test_board = Board(TEST_POSITION2)
        self.assertEqual([], test_board.find_checkers('e1', 'b'))

        black_queen = test_board.state['e5']
        backup_ne4 = test_board.state['e4']
        test_board.remove_piece('e4')
        test_board.recapture_heat()
        # |br|  |bb|bq|bk|bb|bn|  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|
        self.assertTrue(test_board.discover_check('e1', 'e4', 'b'))
        self.assertEqual([black_queen], test_board.find_checkers('e1', 'b'))

        test_board.relocate_piece('c3', 'e3')
        test_board.recapture_heat()
        # |br|  |bb|bq|bk|bb|bn|  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |bn|  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|
        self.assertEqual([], test_board.find_checkers('e1', 'b'))

        test_board.relocate_piece('e3', 'c2')
        test_board.recapture_heat()
        black_knight = test_board.state['c2']
        # |br|  |bb|bq|bk|bb|bn|  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|
        self.assertEqual(set([black_queen, black_knight]), set(test_board.find_checkers('e1', 'b')) )

        test_board.relocate_piece('a8', 'g1')
        test_board.remove_piece('f1')
        test_board.recapture_heat()
        black_rook = test_board.state['g1']
        # |  |  |bb|bq|bk|bb|bn|  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |wr|wn|wb|wq|wk|  |br|wr|
        self.assertEqual(set([black_queen, black_knight, black_rook]), set(test_board.find_checkers('e1', 'b')) )
        self.assertEqual(set(['bq@e5', 'bq@d8', 'br@g1']), set([ str(z) for z in test_board.find_checkers('g5', 'b') ]) )
        self.assertEqual(set(['bq@e5', 'bq@d8', 'bn@g8']), set([ str(z) for z in test_board.find_checkers('f6', 'b') ]) )

    def test_find_pinners(self):
        test_board = Board(TEST_POSITION2)
        # |br|  |bb|bq|bk|bb|bn|  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|wn|wb|wq|wk|wb|  |wr|

        self.assertEqual(set(['b5-d7-e8']), set([ str(z) for z in test_board.find_pinners('e8', 'w') ]))
        self.assertEqual(set(['e5-e4-e1']), set([ str(z) for z in test_board.find_pinners('e1', 'b') ]))
        test_board.relocate_piece('c3', 'e2')
        # test_board.recapture_heat()
        self.assertEqual(set([]), set([ str(z) for z in test_board.find_pinners('e1', 'b') ]))
        test_board.relocate_piece('e2', 'c3')

        test_board.relocate_piece('c8', 'b4')
        self.assertEqual(set(['e5-e4-e1']), set([ str(z) for z in test_board.find_pinners('e1', 'b') ]))
        test_board.relocate_piece('c3', 'a2')
        test_board.relocate_piece('b1', 'c3')
        self.assertEqual(set(['e5-e4-e1', 'b4-c3-e1']), set([ str(z) for z in test_board.find_pinners('e1', 'b') ]))

        test_board.relocate_piece('a8', 'g1')
        self.assertEqual(set(['e5-e4-e1', 'b4-c3-e1', 'g1-f1-e1']), set([ str(z) for z in test_board.find_pinners('e1', 'b') ]))

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
        # undo = test_board.execute_move(capture_move)
        # # move fails
        # self.assertIsNone(undo)
        # ### `execute_move` no longer validates - it assumes the move is prevalidated, thus:
        self.assertFalse(test_board.prevalidate_move(capture_move))

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

        # print(test_game.board.heatness())
        # self.assertEqual(set(['Rg1', 'Rh2', 'Rh3']))


        # the knight at e4, will have the expansion list reduced to []
        self.assertEqual([], test_game.valid_moves_of_piece_at('e4'))

        # with checkers & pinners called at the end of execute move, I need to push that to trigger recalculation of the checkers and pinners for the black
        h1_moves = test_game.valid_moves_of_piece_at('h1')
        test_game.board.execute_move(h1_moves.pop())
        # print(test_game.board)

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
        test_game.board.recapture_heat()
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
        decoded_move = test_game.whites_player.decode_move('O-O')
        # print(king_side_castle, [ getattr(king_side_castle, z) for z in ['piece', 'origin', 'type_', 'destination', 'notation', 'promote_to', 'taken', 'catsling_rook',] ])
        # print(decoded_move, [ getattr(decoded_move, z) for z in ['piece', 'origin', 'type_', 'destination', 'notation', 'promote_to', 'taken', 'catsling_rook',] ])

        def attribute_lister(object_, attributes):
            return [ getattr(object_, z) for z in attributes ]

        move_attributes = ['piece', 'origin', 'type_', 'destination', 'notation', 'promote_to', 'taken', 'catsling_rook',]

        self.assertEqual(attribute_lister(king_side_castle, move_attributes) , attribute_lister(decoded_move, move_attributes))
        # O-O-O because it only decodes against the set, without validation
        queen_side_castle = Move(king,'c', 'c1', 'O-O-O', a_rook)
        decoded_move = test_game.whites_player.decode_move('O[O]O')
        self.assertEqual(attribute_lister(queen_side_castle, move_attributes) , attribute_lister(decoded_move, move_attributes))
        decoded_move = test_game.whites_player.decode_move('OOO')
        self.assertEqual(attribute_lister(queen_side_castle, move_attributes) , attribute_lister(decoded_move, move_attributes))
        decoded_move = test_game.whites_player.decode_move('O,>oOo-0*O')                                                                     #TOFIX?
        # print(attribute_lister(queen_side_castle, move_attributes))
        # print(attribute_lister(decoded_move, move_attributes))
        self.assertEqual(attribute_lister(queen_side_castle, move_attributes) , attribute_lister(decoded_move, move_attributes))
        # The above is left as reminder to rethink the decoding at some point

        #print(zgame.show())
        expected_move = Move(king, 'm', 'f2', 'Kf2')
        decoded_move = test_game.whites_player.decode_move('13. Kf2')
        self.assertEqual(attribute_lister(expected_move, move_attributes) , attribute_lister(decoded_move, move_attributes))
        # self.assertEqual((zgame.zboard.piece_by_sq('e1'),'e1', 'm', 'f2', 'Kf2'), test_player.decode_move('13. Kf2', zgame.turnset()))
        expected_move = Move(test_game.board.state['b5'], 't', 'd7', 'Bxd7', test_game.board.state['d7'])
        decoded_move = test_game.whites_player.decode_move('Bxd7+')
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
        decoded_move = test_game.whites_player.decode_move('h8Q')
        self.assertEqual(attribute_lister(expected_move, no_promo_move_attributes) , attribute_lister(decoded_move, no_promo_move_attributes))

        new_black_knight = Piece('b', 'n', 'g8')
        expected_move = Move(test_game.board.state['h7'], '+', 'g8', 'hxg8N', [new_black_knight, test_game.board.state['g8']])
        decoded_move = test_game.whites_player.decode_move('hxg8N')
        self.assertEqual(attribute_lister(expected_move, no_promo_move_attributes) , attribute_lister(decoded_move, no_promo_move_attributes))
        # assertRaises(exc, fun, *args, **kwds)
        self.assertRaises(DecodeException, test_game.whites_player.decode_move, '999. b8')  # no pawn to reach b8
        self.assertRaises(DecodeException, test_game.whites_player.decode_move, '2 fxgdfgdfgsdfg')  ### destination not on board
        self.assertRaises(DecodeException, test_game.whites_player.decode_move, 'Ra3')  # invalid
        # #e.p.
        expected_move = Move(test_game.board.state['g5'], 'e', 'f6', 'gxf6', test_game.board.state['f5'])
        decoded_move = test_game.whites_player.decode_move('gxf6')
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
        self.assertRaises(SimulationException, test_game.start, False)

    def test_validations_of_castling_move_against_history(self):
        test_game = Game()
        test_game.whites_player.simulate(['e4', 'Nf3', 'Bc4', 'b4', 'Kf1', 'Ke1', 'O-O', 'Nc3'])
        test_game.blacks_player.simulate(['a5', 'a4', 'Nc6', 'axb3', 'h6', 'bxa2', 'h5'])
        self.assertRaises(SimulationException, test_game.start, False)


    def test_non_directional_heat_update(self):
        # NOTE: uses only prevalidate_move, and ommits board.naive_moves, thus moves may cause MoveException
        position = {'h8':'  ', 'h2':'  ', 'h3':'  ', 'h1':'wr', 'h6':'  ', 'h7':'  ', 'h4':'  ', 'h5':'  ', 'd8':'  ', 'a8':'br', 'd6':'  ', 'd7':'bb', 'd4':'  ', 'd5':'  ', 'd2':'  ', 'd3':'  ', 'd1':'  ', 'g7':'  ', 'g6':'  ', 'g5':'  ', 'g4':'  ', 'g3':'  ', 'g2':'  ', 'g1':'  ', 'g8':'  ', 'c8':'  ', 'c3':'bn', 'c2':'  ', 'c1':'  ', 'c7':'  ', 'c6':'  ', 'c5':'  ', 'c4':'  ', 'f1':'  ', 'f2':'  ', 'f3':'  ', 'f4':'  ', 'f5':'  ', 'f6':'  ', 'f7':'  ', 'f8':'  ', 'b4':'  ', 'b5':'wb', 'b6':'  ', 'b7':'wr', 'b1':'  ', 'b2':'  ', 'b3':'  ', 'b8':'  ', 'a1':'wr', 'a3':'  ', 'a2':'  ', 'a5':'  ', 'e8':'bk', 'a7':'  ', 'a6':'  ', 'e5':'  ', 'e4':'  ', 'e7':'  ', 'e6':'  ', 'e1':'wk', 'e3':'  ', 'e2':'wn', 'a4':'  '}
        test_game = Game(board_position=position)
        # |br|  |  |  |bk|  |  |  |
        # |  |wr|  |bb|  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |  |wb|  |  |bq|  |  |  |
        # |  |  |  |  |wn|  |  |  |
        # |  |  |bn|  |  |  |  |  |
        # |  |  |  |  |  |  |  |  |
        # |wr|  |  |  |wk|  |  |wr|
        black_knight = test_game.board.state['c3']

        decoded_move = test_game.whites_player.decode_move('Ke2')
        self.assertFalse(test_game.board.prevalidate_move(decoded_move))

        some_other_white_move = test_game.whites_player.decode_move('Nd4')
        self.assertTrue(test_game.board.prevalidate_move(some_other_white_move))
        test_game.board.execute_move(some_other_white_move)

        knight_away_move = test_game.blacks_player.decode_move('Nxb5')
        self.assertTrue(test_game.board.prevalidate_move(knight_away_move))
        test_game.board.execute_move(knight_away_move)

        decoded_move = test_game.whites_player.decode_move('Ke2')
        self.assertTrue(test_game.board.prevalidate_move(decoded_move))
        test_game.board.execute_move(decoded_move)


class TemporaryGameTest(unittest.TestCase):

    def test_stepping_preventing_enpassant(self):
        position = {'e2':'  ','c8':'  ','e1':'  ','b6':'  ','e8':'bk','e7':'  ','g5':'  ','b1':'  ','a2':'  ','g6':'  ','e6':'  ','f6':'  ','h4':'  ','h7':'bp','g1':'wk','a5':'wp','b2':'  ','d3':'wp','c1':'  ','e3':'  ','c4':'  ','a6':'bp','a4':'  ','d8':'  ','f3':'wp','a8':'br','d2':'  ','c6':'  ','c7':'bp','g8':'  ','d1':'wq','f2':'wp','f1':'wr','g3':'  ','g2':'  ','b8':'  ','c2':'wp','f8':'  ','b4':'bq','b7':'bp','f5':'  ','f4':'  ','d4':'bp','h3':'wp','a3':'  ','c3':'  ','b3':'  ','d7':'  ','b5':'  ','e4':'wn','h6':'  ','d5':'  ','h2':'  ','h8':'br','a1':'wr','h1':'  ','g4':'  ','g7':'bp','h5':'  ','c5':'  ','a7':'bb','f7':'bp','e5':'  ','d6':'  '}
        test_game = Game(board_position=position)
        test_game.whites_player.simulate(['Qe1', 'Rfxe1','f4', 'Ng3', 'Re7', 'Rb1', 'Ra1', 'axb6', 'bxa7'])
        test_game.blacks_player.simulate(['Qxe1', 'OO', 'f5', 'g6', 'Rfc8', 'b6', 'b5', 'Kg8'])
        self.assertRaises(SimulationException, test_game.start, False)

    def test_pawn_side_moving(self):
        position = {'e2':'  ','c8':'  ','e1':'  ','b6':'  ','e8':'bk','e7':'  ','g5':'  ','b1':'  ','a2':'  ','g6':'  ','e6':'  ','f6':'  ','h4':'  ','h7':'bp','g1':'wk','a5':'wp','b2':'  ','d3':'wp','c1':'  ','e3':'  ','c4':'  ','a6':'bp','a4':'  ','d8':'  ','f3':'wp','a8':'br','d2':'  ','c6':'  ','c7':'bp','g8':'  ','d1':'wq','f2':'wp','f1':'wr','g3':'  ','g2':'  ','b8':'  ','c2':'wp','f8':'  ','b4':'bq','b7':'bp','f5':'  ','f4':'  ','d4':'bp','h3':'wp','a3':'  ','c3':'  ','b3':'  ','d7':'  ','b5':'  ','e4':'wn','h6':'  ','d5':'  ','h2':'  ','h8':'br','a1':'wr','h1':'  ','g4':'  ','g7':'bp','h5':'  ','c5':'  ','a7':'bb','f7':'bp','e5':'  ','d6':'  '}
        test_game = Game(board_position=position)
        test_game.whites_player.simulate(['Qe1', 'Rfxe1','f4', 'Ng3', 'Re7', 'Rb1', 'Ra1', 'axb5'])
        test_game.blacks_player.simulate(['Qxe1', 'OO', 'f5', 'g6', 'Rfc8', 'b6', 'b5', 'axb5'])

        # self.assertEqual('stalemate', test_game.start(verbose=False))
        self.assertRaises(SimulationException, test_game.start, False)

    def test_black_capture_promotion(self):
        position = {'d4':'wp','f4':'bb','b6':'  ','c4':'  ','d7':'  ','a5':'wp','d2':'  ','h5':'  ','d3':'  ','h2':'  ','g6':'bp','a3':'  ','f2':'wp','c1':'  ','f3':'  ','e8':'  ','b8':'  ','h1':'  ','a1':'  ','c7':'  ','h6':'  ','d1':'  ','c2':'bp','h7':'bp','c5':'  ','e7':'  ','d8':'  ','a7':'  ','b7':'  ','e3':'  ','d5':'  ','d6':'  ','e2':'wk','f1':'  ','a8':'  ','g1':'  ','g2':'  ','c6':'br','c8':'  ','g3':'  ','b3':'  ','b1':'wr','h8':'  ','f5':'bp','e1':'  ','f7':'bk','e5':'  ','f6':'  ','g7 ':'  ','a4':'  ','h3':'wp','g5':'  ','b5':'  ','g4':'  ','b4':'wn','e6':'  ','c3':'  ','f8':'  ','g8':'  ','e4':'  ','h4':'  ','a2':'  ','b2':'  ','a6':'bp'}
        test_game = Game(board_position=position)
        test_game.whites_player.simulate(['Nxc6'])
        test_game.blacks_player.simulate(['cxb1Q'])

        # self.assertEqual('stalemate', test_game.start(verbose=True))
        self.assertRaises(MoveExhaustException, test_game.start, False)

    def test_black_invalid_notation_for_promotion(self):
        # blacks turn 'b1Q' is decoded as 'cxb1Q'; this is due to "stage 4" of the decode_move method
        position = {'d4':'wp','f4':'bb','b6':'  ','c4':'  ','d7':'  ','a5':'wp','d2':'  ','h5':'  ','d3':'  ','h2':'  ','g6':'bp','a3':'  ','f2':'wp','c1':'  ','f3':'  ','e8':'  ','b8':'  ','h1':'  ','a1':'  ','c7':'  ','h6':'  ','d1':'  ','c2':'bp','h7':'bp','c5':'  ','e7':'  ','d8':'  ','a7':'  ','b7':'  ','e3':'  ','d5':'  ','d6':'  ','e2':'wk','f1':'  ','a8':'  ','g1':'  ','g2':'  ','c6':'br','c8':'  ','g3':'  ','b3':'  ','b1':'wr','h8':'  ','f5':'bp','e1':'  ','f7':'bk','e5':'  ','f6':'  ','g7 ':'  ','a4':'  ','h3':'wp','g5':'  ','b5':'  ','g4':'  ','b4':'wn','e6':'  ','c3':'  ','f8':'  ','g8':'  ','e4':'  ','h4':'  ','a2':'  ','b2':'  ','a6':'bp'}
        test_game = Game(board_position=position)
        test_game.whites_player.simulate(['Nxc6'])
        test_game.blacks_player.simulate(['b1Q'])

        # self.assertEqual('stalemate', test_game.start(verbose=True))
        self.assertRaises(DecodeException, test_game.start, False)

    def test_ambiguous_black_capture_promotion(self):
        position = {'d4':'wp','f4':'bb','b6':'  ','c4':'  ','d7':'  ','a5':'wp','d2':'  ','h5':'  ','d3':'  ','h2':'  ','g6':'bp','a3':'  ','f2':'wp','c1':'  ','f3':'  ','e8':'  ','b8':'  ','h1':'  ','a1':'  ','c7':'  ','h6':'  ','d1':'  ','c2':'bp','h7':'bp','c5':'  ','e7':'  ','d8':'  ','a7':'  ','b7':'  ','e3':'  ','d5':'  ','d6':'  ','e2':'wk','f1':'  ','a8':'  ','g1':'  ','g2':'  ','c6':'br','c8':'  ','g3':'  ','b3':'  ','b1':'wr','h8':'  ','f5':'bp','e1':'  ','f7':'bk','e5':'  ','f6':'  ','g7 ':'  ','a4':'  ','h3':'wp','g5':'  ','b5':'  ','g4':'  ','b4':'wn','e6':'  ','c3':'  ','f8':'  ','g8':'  ','e4':'  ','h4':'  ','a2':'bp','b2':'  ','a6':'bp'}
        test_game = Game(board_position=position)
        test_game.whites_player.simulate(['Nxc6'])
        test_game.blacks_player.simulate(['axb1Q'])

        # self.assertEqual('stalemate', test_game.start(verbose=True))
        self.assertRaises(MoveExhaustException, test_game.start, False)

    @unittest.expectedFailure
    def test_for_disambiguation_in_generated_move_notation(self):
        position = {'h5':'  ', 'g2':'  ', 'f8':'  ', 'g5':'  ', 'd8':'  ', 'd4':'  ', 'c6':'  ', 'e2':'br', 'b6':'  ', 'd3':'  ', 'b3':'  ', 'f1':'  ', 'a8':'  ', 'a7':'  ', 'b1':'  ', 'f3':'  ', 'a6':'  ', 'a2':'  ', 'b2':'  ', 'h6':'  ', 'e3':'  ', 'f6':'  ', 'b7':'  ', 'd5':'  ', 'e4':'wn', 'd6':'  ', 'g7':'  ', 'e6':'  ', 'f2':'  ', 'g6':'  ', 'h7':'  ', 'c1':'  ', 'f4':'  ', 'd2':'  ', 'g1':'  ', 'a1':'wk', 'e8':'  ', 'c8':'  ', 'e5':'  ', 'e7':'br', 'a4':'  ', 'h4':'br', 'b5':'  ', 'c3':'  ', 'b4':'br', 'g3':'  ', 'f7':'  ', 'c7':'  ', 'h1':'  ', 'h8':'bk', 'g8':'  ', 'a3':'  ', 'a5':'  ', 'f5':'  ', 'c4':'  ', 'e1':'  ', 'd7':'  ', 'g4':'  ', 'b8':'  ', 'h2':'  ', 'd1':'  ', 'h3':'  ', 'c5':'  ', 'c2':'  '}
        test_game = Game(board_position=position)

        moves_for_black = []
        for candidate_piece in test_game.board.black:
            expansions = [ z.notation for z in test_game.board.naive_moves(candidate_piece) ]
            moves_for_black.extend(expansions)

        self.assertEqual(len(set(moves_for_black)), len(moves_for_black)) # true if all generated notations are unique
        # this will not lead to issues in decode_move because:
        #   the notation attribute of the generated moves is used only in stage 4 of the decode_move method
        #   stage 4 can be entered only in the following cases:
        #     1. the move is promotion
        #     2. lack of disambiguation in the input move (more than 1 candidate pieces at the end of stage 3)
        #
        #   case (1) - promotion notations include the pawn file, which stage 3 handles as disambiguation, reducing the candidate pieces to one.
        #       The promo character is properly handled in the generated move notation, thus move is correctly identified;
        #   case (2) will correctly demand disambiguation, although for the wrong reason (surplus of matches instead of none)
        #       EXAMPLE:
        #       enter your move: Rxe4
        #       erroneous move('the move is ambiguous. Possible interpretations:[Rxe4, Rxe4, Rxe4, Rxe4]',)
        #       // if notation was proper, the list should have been [Rbxe4, R7xe4, Rhxe4, R2xe4]

        # The disambiguation for generated move notations cannot be in "naive_moves" method because it cannot have visibility of other moves.
        # Apart from decode_move method, the notation attribute of the generated moves could potentially be used in the return of AI methods.
        # Disambiguation could be added to the move notation within such methods when needed. Alternatively that can be done
        # in prompt_input method under the Player calss.

    def test_game_cycle_repetition_broken_by_undo(self):
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
        test_game.whites_player.simulate(['Kd1', '2.Qd2', 'Qe1',         'Qc2', 'Qc1', 'Qd2', 'Qe1', 'Qe2', 'Qe1', 'exit'])
        test_game.blacks_player.simulate(['Qd5', 'Qh1+', 'undo', 'Qb3+', 'Qb7', 'Qd5', 'Qh1', 'Qh5', 'Qh1', 'Qd5', 'exit'])
        self.assertEqual('player w left the game', test_game.start(verbose=False))






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













