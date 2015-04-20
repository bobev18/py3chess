from piece import Piece
from move import Move, MoveException
from board import Board

testboard = Board({'h8': '  ', 'h2': '  ', 'h3': '  ', 'h1': 'wr', 'h6': '  ', 'h7': 'wp', 'h4': '  ', 'h5': '  ', 'd8': 'bq', 'a8': 'br', 'd6': '  ', 'd7': 'bp', 'd4': '  ', 'd5': '  ', 'd2': 'wp', 'd3': '  ', 'd1': 'wq', 'g7': 'bp', 'g6': '  ', 'g5': 'wp', 'g4': '  ', 'g3': '  ', 'g2': '  ', 'g1': '  ', 'g8': 'bn', 'c8': 'bb', 'c3': 'bn', 'c2': 'wp', 'c1': 'wb', 'c7': 'bp', 'c6': '  ', 'c5': '  ', 'c4': '  ', 'f1': 'wb', 'f2': 'wp', 'f3': '  ', 'f4': '  ', 'f5': 'bp', 'f6': '  ', 'f7': '  ', 'f8': 'bb', 'b4': '  ', 'b5': '  ', 'b6': '  ', 'b7': 'bp', 'b1': 'wn', 'b2': 'wp', 'b3': '  ', 'b8': '  ', 'a1': 'wr', 'a3': '  ', 'a2': 'wp', 'a5': '  ', 'e8': 'bk', 'a7': 'bp', 'a6': '  ', 'e5': '  ', 'e4': 'wn', 'e7': 'bp', 'e6': '  ', 'e1': 'wk', 'e3': '  ', 'e2': 'wp', 'a4': '  '})
print(testboard)