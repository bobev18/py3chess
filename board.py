from piece import Piece


ORDERED_BOARD_KEYS = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']
BOARD_KEY_INDEX = {'a1': 0, 'a2': 1, 'a3': 2, 'a4': 3, 'a5': 4, 'a6': 5, 'a7': 6, 'a8': 7, 'b1': 8, 'b2': 9, 'b3': 10, 'b4': 11, 'b5': 12, 'b6': 13, 'b7': 14, 'b8': 15, 'c1': 16, 'c2': 17, 'c3': 18, 'c4': 19, 'c5': 20, 'c6': 21, 'c7': 22, 'c8': 23, 'd1': 24, 'd2': 25, 'd3': 26, 'd4': 27, 'd5': 28, 'd6': 29, 'd7': 30, 'd8': 31, 'e1': 32, 'e2': 33, 'e3': 34, 'e4': 35, 'e5': 36, 'e6': 37, 'e7': 38, 'e8': 39, 'f1': 40, 'f2': 41, 'f3': 42, 'f4': 43, 'f5': 44, 'f6': 45, 'f7': 46, 'f8': 47, 'g1': 48, 'g2': 49, 'g3': 50, 'g4': 51, 'g5': 52, 'g6': 53, 'g7': 54, 'g8': 55, 'h1': 56, 'h2': 57, 'h3': 58, 'h4': 59, 'h5': 60, 'h6': 61, 'h7': 62, 'h8': 63}

EMPTYBOARD = {
              'a8':None, 'b8':None, 'c8':None, 'd8':None, 'e8':None, 'f8':None, 'g8':None, 'h8':None,
              'a7':None, 'b7':None, 'c7':None, 'd7':None, 'e7':None, 'f7':None, 'g7':None, 'h7':None,
              'a6':None, 'b6':None, 'c6':None, 'd6':None, 'e6':None, 'f6':None, 'g6':None, 'h6':None,
              'a5':None, 'b5':None, 'c5':None, 'd5':None, 'e5':None, 'f5':None, 'g5':None, 'h5':None,
              'a4':None, 'b4':None, 'c4':None, 'd4':None, 'e4':None, 'f4':None, 'g4':None, 'h4':None,
              'a3':None, 'b3':None, 'c3':None, 'd3':None, 'e3':None, 'f3':None, 'g3':None, 'h3':None,
              'a2':None, 'b2':None, 'c2':None, 'd2':None, 'e2':None, 'f2':None, 'g2':None, 'h2':None,
              'a1':None, 'b1':None, 'c1':None, 'd1':None, 'e1':None, 'f1':None, 'g1':None, 'h1':None,
              }

INVERSE_HIT_MAP = {
    'a1':{'king': ['a2', 'b2', 'b1'], 'E': ['b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'], 'knight': ['b3', 'c2'], 'wpawn': [], 'NE': ['b2', 'c3', 'd4', 'e5', 'f6', 'g7', 'h8'], 'N': ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'], 'bpawn': ['b2'], 'S': [], 'W': [], 'SW': [], 'SE': [], 'NW': []},
    'a2':{'king': ['a3', 'b3', 'b2', 'b1', 'a1'], 'E': ['b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'], 'knight': ['b4', 'c3', 'c1'], 'wpawn': ['b1'], 'NE': ['b3', 'c4', 'd5', 'e6', 'f7', 'g8'], 'N': ['a3', 'a4', 'a5', 'a6', 'a7', 'a8'], 'bpawn': ['b3'], 'S': ['a1'], 'W': [], 'SW': [], 'SE': ['b1'], 'NW': []},
    'a3':{'king': ['a4', 'b4', 'b3', 'b2', 'a2'], 'E': ['b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'], 'knight': ['b5', 'c4', 'c2', 'b1'], 'wpawn': ['b2'], 'NE': ['b4', 'c5', 'd6', 'e7', 'f8'], 'N': ['a4', 'a5', 'a6', 'a7', 'a8'], 'bpawn': ['b4'], 'S': ['a2', 'a1'], 'W': [], 'SW': [], 'SE': ['b2', 'c1'], 'NW': []},
    'a4':{'king': ['a5', 'b5', 'b4', 'b3', 'a3'], 'E': ['b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'], 'knight': ['b6', 'c5', 'c3', 'b2'], 'wpawn': ['b3'], 'NE': ['b5', 'c6', 'd7', 'e8'], 'N': ['a5', 'a6', 'a7', 'a8'], 'bpawn': ['b5'], 'S': ['a3', 'a2', 'a1'], 'W': [], 'SW': [], 'SE': ['b3', 'c2', 'd1'], 'NW': []},
    'a5':{'king': ['a6', 'b6', 'b5', 'b4', 'a4'], 'E': ['b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'], 'knight': ['b7', 'c6', 'c4', 'b3'], 'wpawn': ['b4'], 'NE': ['b6', 'c7', 'd8'], 'N': ['a6', 'a7', 'a8'], 'bpawn': ['b6'], 'S': ['a4', 'a3', 'a2', 'a1'], 'W': [], 'SW': [], 'SE': ['b4', 'c3', 'd2', 'e1'], 'NW': []},
    'a6':{'king': ['a7', 'b7', 'b6', 'b5', 'a5'], 'E': ['b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'], 'knight': ['b8', 'c7', 'c5', 'b4'], 'wpawn': ['b5'], 'NE': ['b7', 'c8'], 'N': ['a7', 'a8'], 'bpawn': ['b7'], 'S': ['a5', 'a4', 'a3', 'a2', 'a1'], 'W': [], 'SW': [], 'SE': ['b5', 'c4', 'd3', 'e2', 'f1'], 'NW': []},
    'a7':{'king': ['a8', 'b8', 'b7', 'b6', 'a6'], 'E': ['b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'], 'knight': ['c8', 'c6', 'b5'], 'wpawn': ['b6'], 'NE': ['b8'], 'N': ['a8'], 'bpawn': ['b8'], 'S': ['a6', 'a5', 'a4', 'a3', 'a2', 'a1'], 'W': [], 'SW': [], 'SE': ['b6', 'c5', 'd4', 'e3', 'f2', 'g1'], 'NW': []},
    'a8':{'king': ['b8', 'b7', 'a7'], 'E': ['b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'], 'knight': ['c7', 'b6'], 'wpawn': ['b7'], 'NE': [], 'N': [], 'bpawn': [], 'S': ['a7', 'a6', 'a5', 'a4', 'a3', 'a2', 'a1'], 'W': [], 'SW': [], 'SE': ['b7', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1'], 'NW': []},
    'b1':{'king': ['b2', 'c2', 'c1', 'a1', 'a2'], 'E': ['c1', 'd1', 'e1', 'f1', 'g1', 'h1'], 'knight': ['a3', 'c3', 'd2'], 'wpawn': [], 'NE': ['c2', 'd3', 'e4', 'f5', 'g6', 'h7'], 'N': ['b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8'], 'bpawn': ['c2', 'a2'], 'S': [], 'W': ['a1'], 'SW': [], 'SE': [], 'NW': ['a2']},
    'b2':{'king': ['b3', 'c3', 'c2', 'c1', 'b1', 'a1', 'a2', 'a3'], 'E': ['c2', 'd2', 'e2', 'f2', 'g2', 'h2'], 'knight': ['a4', 'c4', 'd3', 'd1'], 'wpawn': ['c1', 'a1'], 'NE': ['c3', 'd4', 'e5', 'f6', 'g7', 'h8'], 'N': ['b3', 'b4', 'b5', 'b6', 'b7', 'b8'], 'bpawn': ['c3', 'a3'], 'S': ['b1'], 'W': ['a2'], 'SW': ['a1'], 'SE': ['c1'], 'NW': ['a3']},
    'b3':{'king': ['b4', 'c4', 'c3', 'c2', 'b2', 'a2', 'a3', 'a4'], 'E': ['c3', 'd3', 'e3', 'f3', 'g3', 'h3'], 'knight': ['a5', 'a1', 'c5', 'd4', 'd2', 'c1'], 'wpawn': ['c2', 'a2'], 'NE': ['c4', 'd5', 'e6', 'f7', 'g8'], 'N': ['b4', 'b5', 'b6', 'b7', 'b8'], 'bpawn': ['c4', 'a4'], 'S': ['b2', 'b1'], 'W': ['a3'], 'SW': ['a2'], 'SE': ['c2', 'd1'], 'NW': ['a4']},
    'b4':{'king': ['b5', 'c5', 'c4', 'c3', 'b3', 'a3', 'a4', 'a5'], 'E': ['c4', 'd4', 'e4', 'f4', 'g4', 'h4'], 'knight': ['a6', 'a2', 'c6', 'd5', 'd3', 'c2'], 'wpawn': ['c3', 'a3'], 'NE': ['c5', 'd6', 'e7', 'f8'], 'N': ['b5', 'b6', 'b7', 'b8'], 'bpawn': ['c5', 'a5'], 'S': ['b3', 'b2', 'b1'], 'W': ['a4'], 'SW': ['a3'], 'SE': ['c3', 'd2', 'e1'], 'NW': ['a5']},
    'b5':{'king': ['b6', 'c6', 'c5', 'c4', 'b4', 'a4', 'a5', 'a6'], 'E': ['c5', 'd5', 'e5', 'f5', 'g5', 'h5'], 'knight': ['a7', 'a3', 'c7', 'd6', 'd4', 'c3'], 'wpawn': ['c4', 'a4'], 'NE': ['c6', 'd7', 'e8'], 'N': ['b6', 'b7', 'b8'], 'bpawn': ['c6', 'a6'], 'S': ['b4', 'b3', 'b2', 'b1'], 'W': ['a5'], 'SW': ['a4'], 'SE': ['c4', 'd3', 'e2', 'f1'], 'NW': ['a6']},
    'b6':{'king': ['b7', 'c7', 'c6', 'c5', 'b5', 'a5', 'a6', 'a7'], 'E': ['c6', 'd6', 'e6', 'f6', 'g6', 'h6'], 'knight': ['a8', 'a4', 'c8', 'd7', 'd5', 'c4'], 'wpawn': ['c5', 'a5'], 'NE': ['c7', 'd8'], 'N': ['b7', 'b8'], 'bpawn': ['c7', 'a7'], 'S': ['b5', 'b4', 'b3', 'b2', 'b1'], 'W': ['a6'], 'SW': ['a5'], 'SE': ['c5', 'd4', 'e3', 'f2', 'g1'], 'NW': ['a7']},
    'b7':{'king': ['b8', 'c8', 'c7', 'c6', 'b6', 'a6', 'a7', 'a8'], 'E': ['c7', 'd7', 'e7', 'f7', 'g7', 'h7'], 'knight': ['a5', 'd8', 'd6', 'c5'], 'wpawn': ['c6', 'a6'], 'NE': ['c8'], 'N': ['b8'], 'bpawn': ['c8', 'a8'], 'S': ['b6', 'b5', 'b4', 'b3', 'b2', 'b1'], 'W': ['a7'], 'SW': ['a6'], 'SE': ['c6', 'd5', 'e4', 'f3', 'g2', 'h1'], 'NW': ['a8']},
    'b8':{'king': ['c8', 'c7', 'b7', 'a7', 'a8'], 'E': ['c8', 'd8', 'e8', 'f8', 'g8', 'h8'], 'knight': ['a6', 'd7', 'c6'], 'wpawn': ['c7', 'a7'], 'NE': [], 'N': [], 'bpawn': [], 'S': ['b7', 'b6', 'b5', 'b4', 'b3', 'b2', 'b1'], 'W': ['a8'], 'SW': ['a7'], 'SE': ['c7', 'd6', 'e5', 'f4', 'g3', 'h2'], 'NW': []},
    'c1':{'king': ['c2', 'd2', 'd1', 'b1', 'b2'], 'E': ['d1', 'e1', 'f1', 'g1', 'h1'], 'knight': ['b3', 'a2', 'd3', 'e2'], 'wpawn': [], 'NE': ['d2', 'e3', 'f4', 'g5', 'h6'], 'N': ['c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'], 'bpawn': ['d2', 'b2'], 'S': [], 'W': ['b1', 'a1'], 'SW': [], 'SE': [], 'NW': ['b2', 'a3']},
    'c2':{'king': ['c3', 'd3', 'd2', 'd1', 'c1', 'b1', 'b2', 'b3'], 'E': ['d2', 'e2', 'f2', 'g2', 'h2'], 'knight': ['b4', 'a3', 'a1', 'd4', 'e3', 'e1'], 'wpawn': ['d1', 'b1'], 'NE': ['d3', 'e4', 'f5', 'g6', 'h7'], 'N': ['c3', 'c4', 'c5', 'c6', 'c7', 'c8'], 'bpawn': ['d3', 'b3'], 'S': ['c1'], 'W': ['b2', 'a2'], 'SW': ['b1'], 'SE': ['d1'], 'NW': ['b3', 'a4']},
    'c3':{'king': ['c4', 'd4', 'd3', 'd2', 'c2', 'b2', 'b3', 'b4'], 'E': ['d3', 'e3', 'f3', 'g3', 'h3'], 'knight': ['b5', 'a4', 'a2', 'b1', 'd5', 'e4', 'e2', 'd1'], 'wpawn': ['d2', 'b2'], 'NE': ['d4', 'e5', 'f6', 'g7', 'h8'], 'N': ['c4', 'c5', 'c6', 'c7', 'c8'], 'bpawn': ['d4', 'b4'], 'S': ['c2', 'c1'], 'W': ['b3', 'a3'], 'SW': ['b2', 'a1'], 'SE': ['d2', 'e1'], 'NW': ['b4', 'a5']},
    'c4':{'king': ['c5', 'd5', 'd4', 'd3', 'c3', 'b3', 'b4', 'b5'], 'E': ['d4', 'e4', 'f4', 'g4', 'h4'], 'knight': ['b6', 'a5', 'a3', 'b2', 'd6', 'e5', 'e3', 'd2'], 'wpawn': ['d3', 'b3'], 'NE': ['d5', 'e6', 'f7', 'g8'], 'N': ['c5', 'c6', 'c7', 'c8'], 'bpawn': ['d5', 'b5'], 'S': ['c3', 'c2', 'c1'], 'W': ['b4', 'a4'], 'SW': ['b3', 'a2'], 'SE': ['d3', 'e2', 'f1'], 'NW': ['b5', 'a6']},
    'c5':{'king': ['c6', 'd6', 'd5', 'd4', 'c4', 'b4', 'b5', 'b6'], 'E': ['d5', 'e5', 'f5', 'g5', 'h5'], 'knight': ['b7', 'a6', 'a4', 'b3', 'd7', 'e6', 'e4', 'd3'], 'wpawn': ['d4', 'b4'], 'NE': ['d6', 'e7', 'f8'], 'N': ['c6', 'c7', 'c8'], 'bpawn': ['d6', 'b6'], 'S': ['c4', 'c3', 'c2', 'c1'], 'W': ['b5', 'a5'], 'SW': ['b4', 'a3'], 'SE': ['d4', 'e3', 'f2', 'g1'], 'NW': ['b6', 'a7']},
    'c6':{'king': ['c7', 'd7', 'd6', 'd5', 'c5', 'b5', 'b6', 'b7'], 'E': ['d6', 'e6', 'f6', 'g6', 'h6'], 'knight': ['b8', 'a7', 'a5', 'b4', 'd8', 'e7', 'e5', 'd4'], 'wpawn': ['d5', 'b5'], 'NE': ['d7', 'e8'], 'N': ['c7', 'c8'], 'bpawn': ['d7', 'b7'], 'S': ['c5', 'c4', 'c3', 'c2', 'c1'], 'W': ['b6', 'a6'], 'SW': ['b5', 'a4'], 'SE': ['d5', 'e4', 'f3', 'g2', 'h1'], 'NW': ['b7', 'a8']},
    'c7':{'king': ['c8', 'd8', 'd7', 'd6', 'c6', 'b6', 'b7', 'b8'], 'E': ['d7', 'e7', 'f7', 'g7', 'h7'], 'knight': ['a8', 'a6', 'b5', 'e8', 'e6', 'd5'], 'wpawn': ['d6', 'b6'], 'NE': ['d8'], 'N': ['c8'], 'bpawn': ['d8', 'b8'], 'S': ['c6', 'c5', 'c4', 'c3', 'c2', 'c1'], 'W': ['b7', 'a7'], 'SW': ['b6', 'a5'], 'SE': ['d6', 'e5', 'f4', 'g3', 'h2'], 'NW': ['b8']},
    'c8':{'king': ['d8', 'd7', 'c7', 'b7', 'b8'], 'E': ['d8', 'e8', 'f8', 'g8', 'h8'], 'knight': ['a7', 'b6', 'e7', 'd6'], 'wpawn': ['d7', 'b7'], 'NE': [], 'N': [], 'bpawn': [], 'S': ['c7', 'c6', 'c5', 'c4', 'c3', 'c2', 'c1'], 'W': ['b8', 'a8'], 'SW': ['b7', 'a6'], 'SE': ['d7', 'e6', 'f5', 'g4', 'h3'], 'NW': []},
    'd1':{'king': ['d2', 'e2', 'e1', 'c1', 'c2'], 'E': ['e1', 'f1', 'g1', 'h1'], 'knight': ['c3', 'b2', 'e3', 'f2'], 'wpawn': [], 'NE': ['e2', 'f3', 'g4', 'h5'], 'N': ['d2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8'], 'bpawn': ['e2', 'c2'], 'S': [], 'W': ['c1', 'b1', 'a1'], 'SW': [], 'SE': [], 'NW': ['c2', 'b3', 'a4']},
    'd2':{'king': ['d3', 'e3', 'e2', 'e1', 'd1', 'c1', 'c2', 'c3'], 'E': ['e2', 'f2', 'g2', 'h2'], 'knight': ['c4', 'b3', 'b1', 'e4', 'f3', 'f1'], 'wpawn': ['e1', 'c1'], 'NE': ['e3', 'f4', 'g5', 'h6'], 'N': ['d3', 'd4', 'd5', 'd6', 'd7', 'd8'], 'bpawn': ['e3', 'c3'], 'S': ['d1'], 'W': ['c2', 'b2', 'a2'], 'SW': ['c1'], 'SE': ['e1'], 'NW': ['c3', 'b4', 'a5']},
    'd3':{'king': ['d4', 'e4', 'e3', 'e2', 'd2', 'c2', 'c3', 'c4'], 'E': ['e3', 'f3', 'g3', 'h3'], 'knight': ['c5', 'b4', 'b2', 'c1', 'e5', 'f4', 'f2', 'e1'], 'wpawn': ['e2', 'c2'], 'NE': ['e4', 'f5', 'g6', 'h7'], 'N': ['d4', 'd5', 'd6', 'd7', 'd8'], 'bpawn': ['e4', 'c4'], 'S': ['d2', 'd1'], 'W': ['c3', 'b3', 'a3'], 'SW': ['c2', 'b1'], 'SE': ['e2', 'f1'], 'NW': ['c4', 'b5', 'a6']},
    'd4':{'king': ['d5', 'e5', 'e4', 'e3', 'd3', 'c3', 'c4', 'c5'], 'E': ['e4', 'f4', 'g4', 'h4'], 'knight': ['c6', 'b5', 'b3', 'c2', 'e6', 'f5', 'f3', 'e2'], 'wpawn': ['e3', 'c3'], 'NE': ['e5', 'f6', 'g7', 'h8'], 'N': ['d5', 'd6', 'd7', 'd8'], 'bpawn': ['e5', 'c5'], 'S': ['d3', 'd2', 'd1'], 'W': ['c4', 'b4', 'a4'], 'SW': ['c3', 'b2', 'a1'], 'SE': ['e3', 'f2', 'g1'], 'NW': ['c5', 'b6', 'a7']},
    'd5':{'king': ['d6', 'e6', 'e5', 'e4', 'd4', 'c4', 'c5', 'c6'], 'E': ['e5', 'f5', 'g5', 'h5'], 'knight': ['c7', 'b6', 'b4', 'c3', 'e7', 'f6', 'f4', 'e3'], 'wpawn': ['e4', 'c4'], 'NE': ['e6', 'f7', 'g8'], 'N': ['d6', 'd7', 'd8'], 'bpawn': ['e6', 'c6'], 'S': ['d4', 'd3', 'd2', 'd1'], 'W': ['c5', 'b5', 'a5'], 'SW': ['c4', 'b3', 'a2'], 'SE': ['e4', 'f3', 'g2', 'h1'], 'NW': ['c6', 'b7', 'a8']},
    'd6':{'king': ['d7', 'e7', 'e6', 'e5', 'd5', 'c5', 'c6', 'c7'], 'E': ['e6', 'f6', 'g6', 'h6'], 'knight': ['c8', 'b7', 'b5', 'c4', 'e8', 'f7', 'f5', 'e4'], 'wpawn': ['e5', 'c5'], 'NE': ['e7', 'f8'], 'N': ['d7', 'd8'], 'bpawn': ['e7', 'c7'], 'S': ['d5', 'd4', 'd3', 'd2', 'd1'], 'W': ['c6', 'b6', 'a6'], 'SW': ['c5', 'b4', 'a3'], 'SE': ['e5', 'f4', 'g3', 'h2'], 'NW': ['c7', 'b8']},
    'd7':{'king': ['d8', 'e8', 'e7', 'e6', 'd6', 'c6', 'c7', 'c8'], 'E': ['e7', 'f7', 'g7', 'h7'], 'knight': ['b8', 'b6', 'c5', 'f8', 'f6', 'e5'], 'wpawn': ['e6', 'c6'], 'NE': ['e8'], 'N': ['d8'], 'bpawn': ['e8', 'c8'], 'S': ['d6', 'd5', 'd4', 'd3', 'd2', 'd1'], 'W': ['c7', 'b7', 'a7'], 'SW': ['c6', 'b5', 'a4'], 'SE': ['e6', 'f5', 'g4', 'h3'], 'NW': ['c8']},
    'd8':{'king': ['e8', 'e7', 'd7', 'c7', 'c8'], 'E': ['e8', 'f8', 'g8', 'h8'], 'knight': ['b7', 'c6', 'f7', 'e6'], 'wpawn': ['e7', 'c7'], 'NE': [], 'N': [], 'bpawn': [], 'S': ['d7', 'd6', 'd5', 'd4', 'd3', 'd2', 'd1'], 'W': ['c8', 'b8', 'a8'], 'SW': ['c7', 'b6', 'a5'], 'SE': ['e7', 'f6', 'g5', 'h4'], 'NW': []},
    'e1':{'king': ['e2', 'f2', 'f1', 'd1', 'd2'], 'E': ['f1', 'g1', 'h1'], 'knight': ['d3', 'c2', 'f3', 'g2'], 'wpawn': [], 'NE': ['f2', 'g3', 'h4'], 'N': ['e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8'], 'bpawn': ['f2', 'd2'], 'S': [], 'W': ['d1', 'c1', 'b1', 'a1'], 'SW': [], 'SE': [], 'NW': ['d2', 'c3', 'b4', 'a5']},
    'e2':{'king': ['e3', 'f3', 'f2', 'f1', 'e1', 'd1', 'd2', 'd3'], 'E': ['f2', 'g2', 'h2'], 'knight': ['d4', 'c3', 'c1', 'f4', 'g3', 'g1'], 'wpawn': ['f1', 'd1'], 'NE': ['f3', 'g4', 'h5'], 'N': ['e3', 'e4', 'e5', 'e6', 'e7', 'e8'], 'bpawn': ['f3', 'd3'], 'S': ['e1'], 'W': ['d2', 'c2', 'b2', 'a2'], 'SW': ['d1'], 'SE': ['f1'], 'NW': ['d3', 'c4', 'b5', 'a6']},
    'e3':{'king': ['e4', 'f4', 'f3', 'f2', 'e2', 'd2', 'd3', 'd4'], 'E': ['f3', 'g3', 'h3'], 'knight': ['d5', 'c4', 'c2', 'd1', 'f5', 'g4', 'g2', 'f1'], 'wpawn': ['f2', 'd2'], 'NE': ['f4', 'g5', 'h6'], 'N': ['e4', 'e5', 'e6', 'e7', 'e8'], 'bpawn': ['f4', 'd4'], 'S': ['e2', 'e1'], 'W': ['d3', 'c3', 'b3', 'a3'], 'SW': ['d2', 'c1'], 'SE': ['f2', 'g1'], 'NW': ['d4', 'c5', 'b6', 'a7']},
    'e4':{'king': ['e5', 'f5', 'f4', 'f3', 'e3', 'd3', 'd4', 'd5'], 'E': ['f4', 'g4', 'h4'], 'knight': ['d6', 'c5', 'c3', 'd2', 'f6', 'g5', 'g3', 'f2'], 'wpawn': ['f3', 'd3'], 'NE': ['f5', 'g6', 'h7'], 'N': ['e5', 'e6', 'e7', 'e8'], 'bpawn': ['f5', 'd5'], 'S': ['e3', 'e2', 'e1'], 'W': ['d4', 'c4', 'b4', 'a4'], 'SW': ['d3', 'c2', 'b1'], 'SE': ['f3', 'g2', 'h1'], 'NW': ['d5', 'c6', 'b7', 'a8']},
    'e5':{'king': ['e6', 'f6', 'f5', 'f4', 'e4', 'd4', 'd5', 'd6'], 'E': ['f5', 'g5', 'h5'], 'knight': ['d7', 'c6', 'c4', 'd3', 'f7', 'g6', 'g4', 'f3'], 'wpawn': ['f4', 'd4'], 'NE': ['f6', 'g7', 'h8'], 'N': ['e6', 'e7', 'e8'], 'bpawn': ['f6', 'd6'], 'S': ['e4', 'e3', 'e2', 'e1'], 'W': ['d5', 'c5', 'b5', 'a5'], 'SW': ['d4', 'c3', 'b2', 'a1'], 'SE': ['f4', 'g3', 'h2'], 'NW': ['d6', 'c7', 'b8']},
    'e6':{'king': ['e7', 'f7', 'f6', 'f5', 'e5', 'd5', 'd6', 'd7'], 'E': ['f6', 'g6', 'h6'], 'knight': ['d8', 'c7', 'c5', 'd4', 'f8', 'g7', 'g5', 'f4'], 'wpawn': ['f5', 'd5'], 'NE': ['f7', 'g8'], 'N': ['e7', 'e8'], 'bpawn': ['f7', 'd7'], 'S': ['e5', 'e4', 'e3', 'e2', 'e1'], 'W': ['d6', 'c6', 'b6', 'a6'], 'SW': ['d5', 'c4', 'b3', 'a2'], 'SE': ['f5', 'g4', 'h3'], 'NW': ['d7', 'c8']},
    'e7':{'king': ['e8', 'f8', 'f7', 'f6', 'e6', 'd6', 'd7', 'd8'], 'E': ['f7', 'g7', 'h7'], 'knight': ['c8', 'c6', 'd5', 'g8', 'g6', 'f5'], 'wpawn': ['f6', 'd6'], 'NE': ['f8'], 'N': ['e8'], 'bpawn': ['f8', 'd8'], 'S': ['e6', 'e5', 'e4', 'e3', 'e2', 'e1'], 'W': ['d7', 'c7', 'b7', 'a7'], 'SW': ['d6', 'c5', 'b4', 'a3'], 'SE': ['f6', 'g5', 'h4'], 'NW': ['d8']},
    'e8':{'king': ['f8', 'f7', 'e7', 'd7', 'd8'], 'E': ['f8', 'g8', 'h8'], 'knight': ['c7', 'd6', 'g7', 'f6'], 'wpawn': ['f7', 'd7'], 'NE': [], 'N': [], 'bpawn': [], 'S': ['e7', 'e6', 'e5', 'e4', 'e3', 'e2', 'e1'], 'W': ['d8', 'c8', 'b8', 'a8'], 'SW': ['d7', 'c6', 'b5', 'a4'], 'SE': ['f7', 'g6', 'h5'], 'NW': []},
    'f1':{'king': ['f2', 'g2', 'g1', 'e1', 'e2'], 'E': ['g1', 'h1'], 'knight': ['e3', 'd2', 'g3', 'h2'], 'wpawn': [], 'NE': ['g2', 'h3'], 'N': ['f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8'], 'bpawn': ['g2', 'e2'], 'S': [], 'W': ['e1', 'd1', 'c1', 'b1', 'a1'], 'SW': [], 'SE': [], 'NW': ['e2', 'd3', 'c4', 'b5', 'a6']},
    'f2':{'king': ['f3', 'g3', 'g2', 'g1', 'f1', 'e1', 'e2', 'e3'], 'E': ['g2', 'h2'], 'knight': ['e4', 'd3', 'd1', 'g4', 'h3', 'h1'], 'wpawn': ['g1', 'e1'], 'NE': ['g3', 'h4'], 'N': ['f3', 'f4', 'f5', 'f6', 'f7', 'f8'], 'bpawn': ['g3', 'e3'], 'S': ['f1'], 'W': ['e2', 'd2', 'c2', 'b2', 'a2'], 'SW': ['e1'], 'SE': ['g1'], 'NW': ['e3', 'd4', 'c5', 'b6', 'a7']},
    'f3':{'king': ['f4', 'g4', 'g3', 'g2', 'f2', 'e2', 'e3', 'e4'], 'E': ['g3', 'h3'], 'knight': ['e5', 'd4', 'd2', 'e1', 'g5', 'h4', 'h2', 'g1'], 'wpawn': ['g2', 'e2'], 'NE': ['g4', 'h5'], 'N': ['f4', 'f5', 'f6', 'f7', 'f8'], 'bpawn': ['g4', 'e4'], 'S': ['f2', 'f1'], 'W': ['e3', 'd3', 'c3', 'b3', 'a3'], 'SW': ['e2', 'd1'], 'SE': ['g2', 'h1'], 'NW': ['e4', 'd5', 'c6', 'b7', 'a8']},
    'f4':{'king': ['f5', 'g5', 'g4', 'g3', 'f3', 'e3', 'e4', 'e5'], 'E': ['g4', 'h4'], 'knight': ['e6', 'd5', 'd3', 'e2', 'g6', 'h5', 'h3', 'g2'], 'wpawn': ['g3', 'e3'], 'NE': ['g5', 'h6'], 'N': ['f5', 'f6', 'f7', 'f8'], 'bpawn': ['g5', 'e5'], 'S': ['f3', 'f2', 'f1'], 'W': ['e4', 'd4', 'c4', 'b4', 'a4'], 'SW': ['e3', 'd2', 'c1'], 'SE': ['g3', 'h2'], 'NW': ['e5', 'd6', 'c7', 'b8']},
    'f5':{'king': ['f6', 'g6', 'g5', 'g4', 'f4', 'e4', 'e5', 'e6'], 'E': ['g5', 'h5'], 'knight': ['e7', 'd6', 'd4', 'e3', 'g7', 'h6', 'h4', 'g3'], 'wpawn': ['g4', 'e4'], 'NE': ['g6', 'h7'], 'N': ['f6', 'f7', 'f8'], 'bpawn': ['g6', 'e6'], 'S': ['f4', 'f3', 'f2', 'f1'], 'W': ['e5', 'd5', 'c5', 'b5', 'a5'], 'SW': ['e4', 'd3', 'c2', 'b1'], 'SE': ['g4', 'h3'], 'NW': ['e6', 'd7', 'c8']},
    'f6':{'king': ['f7', 'g7', 'g6', 'g5', 'f5', 'e5', 'e6', 'e7'], 'E': ['g6', 'h6'], 'knight': ['e8', 'd7', 'd5', 'e4', 'g8', 'h7', 'h5', 'g4'], 'wpawn': ['g5', 'e5'], 'NE': ['g7', 'h8'], 'N': ['f7', 'f8'], 'bpawn': ['g7', 'e7'], 'S': ['f5', 'f4', 'f3', 'f2', 'f1'], 'W': ['e6', 'd6', 'c6', 'b6', 'a6'], 'SW': ['e5', 'd4', 'c3', 'b2', 'a1'], 'SE': ['g5', 'h4'], 'NW': ['e7', 'd8']},
    'f7':{'king': ['f8', 'g8', 'g7', 'g6', 'f6', 'e6', 'e7', 'e8'], 'E': ['g7', 'h7'], 'knight': ['d8', 'd6', 'e5', 'h8', 'h6', 'g5'], 'wpawn': ['g6', 'e6'], 'NE': ['g8'], 'N': ['f8'], 'bpawn': ['g8', 'e8'], 'S': ['f6', 'f5', 'f4', 'f3', 'f2', 'f1'], 'W': ['e7', 'd7', 'c7', 'b7', 'a7'], 'SW': ['e6', 'd5', 'c4', 'b3', 'a2'], 'SE': ['g6', 'h5'], 'NW': ['e8']},
    'f8':{'king': ['g8', 'g7', 'f7', 'e7', 'e8'], 'E': ['g8', 'h8'], 'knight': ['d7', 'e6', 'h7', 'g6'], 'wpawn': ['g7', 'e7'], 'NE': [], 'N': [], 'bpawn': [], 'S': ['f7', 'f6', 'f5', 'f4', 'f3', 'f2', 'f1'], 'W': ['e8', 'd8', 'c8', 'b8', 'a8'], 'SW': ['e7', 'd6', 'c5', 'b4', 'a3'], 'SE': ['g7', 'h6'], 'NW': []},
    'g1':{'king': ['g2', 'h2', 'h1', 'f1', 'f2'], 'E': ['h1'], 'knight': ['f3', 'e2', 'h3'], 'wpawn': [], 'NE': ['h2'], 'N': ['g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8'], 'bpawn': ['h2', 'f2'], 'S': [], 'W': ['f1', 'e1', 'd1', 'c1', 'b1', 'a1'], 'SW': [], 'SE': [], 'NW': ['f2', 'e3', 'd4', 'c5', 'b6', 'a7']},
    'g2':{'king': ['g3', 'h3', 'h2', 'h1', 'g1', 'f1', 'f2', 'f3'], 'E': ['h2'], 'knight': ['f4', 'e3', 'e1', 'h4'], 'wpawn': ['h1', 'f1'], 'NE': ['h3'], 'N': ['g3', 'g4', 'g5', 'g6', 'g7', 'g8'], 'bpawn': ['h3', 'f3'], 'S': ['g1'], 'W': ['f2', 'e2', 'd2', 'c2', 'b2', 'a2'], 'SW': ['f1'], 'SE': ['h1'], 'NW': ['f3', 'e4', 'd5', 'c6', 'b7', 'a8']},
    'g3':{'king': ['g4', 'h4', 'h3', 'h2', 'g2', 'f2', 'f3', 'f4'], 'E': ['h3'], 'knight': ['f5', 'e4', 'e2', 'f1', 'h5', 'h1'], 'wpawn': ['h2', 'f2'], 'NE': ['h4'], 'N': ['g4', 'g5', 'g6', 'g7', 'g8'], 'bpawn': ['h4', 'f4'], 'S': ['g2', 'g1'], 'W': ['f3', 'e3', 'd3', 'c3', 'b3', 'a3'], 'SW': ['f2', 'e1'], 'SE': ['h2'], 'NW': ['f4', 'e5', 'd6', 'c7', 'b8']},
    'g4':{'king': ['g5', 'h5', 'h4', 'h3', 'g3', 'f3', 'f4', 'f5'], 'E': ['h4'], 'knight': ['f6', 'e5', 'e3', 'f2', 'h6', 'h2'], 'wpawn': ['h3', 'f3'], 'NE': ['h5'], 'N': ['g5', 'g6', 'g7', 'g8'], 'bpawn': ['h5', 'f5'], 'S': ['g3', 'g2', 'g1'], 'W': ['f4', 'e4', 'd4', 'c4', 'b4', 'a4'], 'SW': ['f3', 'e2', 'd1'], 'SE': ['h3'], 'NW': ['f5', 'e6', 'd7', 'c8']},
    'g5':{'king': ['g6', 'h6', 'h5', 'h4', 'g4', 'f4', 'f5', 'f6'], 'E': ['h5'], 'knight': ['f7', 'e6', 'e4', 'f3', 'h7', 'h3'], 'wpawn': ['h4', 'f4'], 'NE': ['h6'], 'N': ['g6', 'g7', 'g8'], 'bpawn': ['h6', 'f6'], 'S': ['g4', 'g3', 'g2', 'g1'], 'W': ['f5', 'e5', 'd5', 'c5', 'b5', 'a5'], 'SW': ['f4', 'e3', 'd2', 'c1'], 'SE': ['h4'], 'NW': ['f6', 'e7', 'd8']},
    'g6':{'king': ['g7', 'h7', 'h6', 'h5', 'g5', 'f5', 'f6', 'f7'], 'E': ['h6'], 'knight': ['f8', 'e7', 'e5', 'f4', 'h8', 'h4'], 'wpawn': ['h5', 'f5'], 'NE': ['h7'], 'N': ['g7', 'g8'], 'bpawn': ['h7', 'f7'], 'S': ['g5', 'g4', 'g3', 'g2', 'g1'], 'W': ['f6', 'e6', 'd6', 'c6', 'b6', 'a6'], 'SW': ['f5', 'e4', 'd3', 'c2', 'b1'], 'SE': ['h5'], 'NW': ['f7', 'e8']},
    'g7':{'king': ['g8', 'h8', 'h7', 'h6', 'g6', 'f6', 'f7', 'f8'], 'E': ['h7'], 'knight': ['e8', 'e6', 'f5', 'h5'], 'wpawn': ['h6', 'f6'], 'NE': ['h8'], 'N': ['g8'], 'bpawn': ['h8', 'f8'], 'S': ['g6', 'g5', 'g4', 'g3', 'g2', 'g1'], 'W': ['f7', 'e7', 'd7', 'c7', 'b7', 'a7'], 'SW': ['f6', 'e5', 'd4', 'c3', 'b2', 'a1'], 'SE': ['h6'], 'NW': ['f8']},
    'g8':{'king': ['h8', 'h7', 'g7', 'f7', 'f8'], 'E': ['h8'], 'knight': ['e7', 'f6', 'h6'], 'wpawn': ['h7', 'f7'], 'NE': [], 'N': [], 'bpawn': [], 'S': ['g7', 'g6', 'g5', 'g4', 'g3', 'g2', 'g1'], 'W': ['f8', 'e8', 'd8', 'c8', 'b8', 'a8'], 'SW': ['f7', 'e6', 'd5', 'c4', 'b3', 'a2'], 'SE': ['h7'], 'NW': []},
    'h1':{'king': ['h2', 'g1', 'g2'], 'E': [], 'knight': ['g3', 'f2'], 'wpawn': [], 'NE': [], 'N': ['h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'], 'bpawn': ['g2'], 'S': [], 'W': ['g1', 'f1', 'e1', 'd1', 'c1', 'b1', 'a1'], 'SW': [], 'SE': [], 'NW': ['g2', 'f3', 'e4', 'd5', 'c6', 'b7', 'a8']},
    'h2':{'king': ['h3', 'h1', 'g1', 'g2', 'g3'], 'E': [], 'knight': ['g4', 'f3', 'f1'], 'wpawn': ['g1'], 'NE': [], 'N': ['h3', 'h4', 'h5', 'h6', 'h7', 'h8'], 'bpawn': ['g3'], 'S': ['h1'], 'W': ['g2', 'f2', 'e2', 'd2', 'c2', 'b2', 'a2'], 'SW': ['g1'], 'SE': [], 'NW': ['g3', 'f4', 'e5', 'd6', 'c7', 'b8']},
    'h3':{'king': ['h4', 'h2', 'g2', 'g3', 'g4'], 'E': [], 'knight': ['g5', 'f4', 'f2', 'g1'], 'wpawn': ['g2'], 'NE': [], 'N': ['h4', 'h5', 'h6', 'h7', 'h8'], 'bpawn': ['g4'], 'S': ['h2', 'h1'], 'W': ['g3', 'f3', 'e3', 'd3', 'c3', 'b3', 'a3'], 'SW': ['g2', 'f1'], 'SE': [], 'NW': ['g4', 'f5', 'e6', 'd7', 'c8']},
    'h4':{'king': ['h5', 'h3', 'g3', 'g4', 'g5'], 'E': [], 'knight': ['g6', 'f5', 'f3', 'g2'], 'wpawn': ['g3'], 'NE': [], 'N': ['h5', 'h6', 'h7', 'h8'], 'bpawn': ['g5'], 'S': ['h3', 'h2', 'h1'], 'W': ['g4', 'f4', 'e4', 'd4', 'c4', 'b4', 'a4'], 'SW': ['g3', 'f2', 'e1'], 'SE': [], 'NW': ['g5', 'f6', 'e7', 'd8']},
    'h5':{'king': ['h6', 'h4', 'g4', 'g5', 'g6'], 'E': [], 'knight': ['g7', 'f6', 'f4', 'g3'], 'wpawn': ['g4'], 'NE': [], 'N': ['h6', 'h7', 'h8'], 'bpawn': ['g6'], 'S': ['h4', 'h3', 'h2', 'h1'], 'W': ['g5', 'f5', 'e5', 'd5', 'c5', 'b5', 'a5'], 'SW': ['g4', 'f3', 'e2', 'd1'], 'SE': [], 'NW': ['g6', 'f7', 'e8']},
    'h6':{'king': ['h7', 'h5', 'g5', 'g6', 'g7'], 'E': [], 'knight': ['g8', 'f7', 'f5', 'g4'], 'wpawn': ['g5'], 'NE': [], 'N': ['h7', 'h8'], 'bpawn': ['g7'], 'S': ['h5', 'h4', 'h3', 'h2', 'h1'], 'W': ['g6', 'f6', 'e6', 'd6', 'c6', 'b6', 'a6'], 'SW': ['g5', 'f4', 'e3', 'd2', 'c1'], 'SE': [], 'NW': ['g7', 'f8']},
    'h7':{'king': ['h8', 'h6', 'g6', 'g7', 'g8'], 'E': [], 'knight': ['f8', 'f6', 'g5'], 'wpawn': ['g6'], 'NE': [], 'N': ['h8'], 'bpawn': ['g8'], 'S': ['h6', 'h5', 'h4', 'h3', 'h2', 'h1'], 'W': ['g7', 'f7', 'e7', 'd7', 'c7', 'b7', 'a7'], 'SW': ['g6', 'f5', 'e4', 'd3', 'c2', 'b1'], 'SE': [], 'NW': ['g8']},
    'h8':{'king': ['h7', 'g7', 'g8'], 'E': [], 'knight': ['f7', 'g6'], 'wpawn': ['g7'], 'NE': [], 'N': [], 'bpawn': [], 'S': ['h7', 'h6', 'h5', 'h4', 'h3', 'h2', 'h1'], 'W': ['g8', 'f8', 'e8', 'd8', 'c8', 'b8', 'a8'], 'SW': ['g7', 'f6', 'e5', 'd4', 'c3', 'b2', 'a1'], 'SE': [], 'NW': []},
}

def neggate_direction(direction):
    if direction == 'N': return 'S'
    if direction == 'S': return 'N'
    if direction == 'E': return 'W'
    if direction == 'W': return 'E'
    if direction == 'NE': return 'SW'
    if direction == 'SW': return 'NE'
    if direction == 'SE': return 'NW'
    if direction == 'NW': return 'SE'

class MoveException(Exception):
    def __init__(self, *args):
        # *args is used to get a list of the parameters passed
        self.args = [a for a in args]

class Pin():
    def __init__(self, pinner, pinnee, king_location, direction):
        self.pinner = pinner
        self.pinnee = pinnee
        self.color = pinnee.color
        self.king_location = king_location
        self.direction = neggate_direction(direction)

    def __repr__(self):
        return self.pinner.location + '-' + self.pinnee.location + '-' + self.king_location

class Check():
    def __init__(self, checker, king_location, direction=None):
        self.checker = checker
        self.king_location = king_location
        if direction:
            self.direction = neggate_direction(direction)
        else:
            self.direction = None

    def __repr__(self):
        return self.checker.location + '-' + king_location

class Board():
    def __init__(self, construction_state={}):
        self.white = []
        self.black = []
        self.all = []
        self.heat = {'w': { z:0 for z in ORDERED_BOARD_KEYS }, 'b': { z:0 for z in ORDERED_BOARD_KEYS }}
        self.state = EMPTYBOARD.copy()
        self.hashstate = ' '*64
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
                    piece = self.state[chr(j)+str(i)].designation
                except AttributeError:
                    piece = '  '
                result += piece + '|'
            result += '\n'
        return result

    def heatness(self, indent=0):
        result = '\n'
        for i in range(8,0,-1):
            result += ' '*indent + '|'
            wh = ''
            bh = ''
            for j in range(97,105):
                loc = chr(j)+str(i)
                if self.heat['w'][loc] != 0:
                    wh += str(self.heat['w'][loc])
                else:
                    wh += ' '
                if self.heat['b'][loc] != 0:
                    bh += str(self.heat['b'][loc])
                else:
                    bh += ' '
                wh += '|'
                bh += '|'
            result += wh + '          |' + bh + '\n'
        return result

    def debug_heatness(self, heat, indent=0):
        result = '\n'
        for i in range(8,0,-1):
            result += ' '*indent + '|'
            wh = ''
            bh = ''
            for j in range(97,105):
                loc = chr(j)+str(i)
                if loc in heat:
                    wh += str(heat.count(loc))
                else:
                    wh += ' '
                wh += '|'
            result += wh + '\n'
        return result


    def export(self):
        return { k: str(v) if v else '  ' for (k,v) in self.state.items() }

    def pieces_of_color(self, color):
        if color == 'w':
            return self.white
        else:
            return self.black

    def spawn_pieces(self, init_state):
        # 'state' here should be the input of the constructor, which should be dict of string values!
        for square in init_state.keys():
            if init_state[square] != '  ':
                self.add_piece(init_state[square][0], init_state[square][1], square, False)
                if init_state[square] == 'wk':
                    self.white_king = self.state[square]
                if init_state[square] == 'bk':
                    self.black_king = self.state[square]
        self.heat = {'w': { z:0 for z in ORDERED_BOARD_KEYS }, 'b': { z:0 for z in ORDERED_BOARD_KEYS }}
        # generate heat
        for piece in self.all:
            piece.update_heat()
        # generate heat needs to be prior to update_incheck, because update_incheck calls find_checkers/pinners, which rely on heat
        self.update_incheck('w')
        self.update_incheck('b')
        # ^^^ the update_incheck order is significant because the self.checks & self.pinners do not hold separate spaces for each color but are overwritten!!!

    def add_piece(self, color, type_=None, location=None, not_spawn=True):
        if isinstance(color, Piece):
            new_piece = color
            location = new_piece.location
        else:
            try:  # for CT@XY
                type_ = color[1]
                location = color[-2:]
                color = color[0]
            except IndexError:
                pass

            if self.state[location]:
                message = 'Are you blind - there is another piece at that spot: ' + repr(self.state[location])
                raise MoveException(message)

            new_piece = Piece(self, color, type_, location)

        self.state[location] = new_piece
        affected = self.find_blockers(location)           # note that determining affected pieces should be after making chage to the self.state !!!

        for affectee in affected:
            new_piece.block(*affectee)
            self.state[affectee[0]].block(location, neggate_direction(affectee[1]))
            if not_spawn:
                self.state[affectee[0]].update_heat()

        self.all.append(new_piece)
        if new_piece.color == 'w':
            self.white.append(new_piece)
        else:
            self.black.append(new_piece)
        index = BOARD_KEY_INDEX[location]
        self.hashstate = self.hashstate[:index] + new_piece.hashtype + self.hashstate[index+1:]
        # return set(affected).union([new_piece])
        # return set([new_piece]) # ??? to cause heat update?
        if not_spawn:
            new_piece.update_heat()      # the actor piece heat can be updated here

    def remove_piece(self, location_):
        if isinstance(location_, Piece):
            piece = location_
            location = piece.location
        else:
            piece = self.state[location_]
            location = location_

        if not piece:
            message = 'Trying to move the air at ' + location
            raise MoveException(message)

        captured = self.state[location]
        captured.clear_heat()
        captured.old_heat = []          # reset the internal heat of the captured piece, because undo will use the same object
        self.state[location] = None
        affected = self.find_unblockers(location)
        for affectee in affected.keys():
            self.state[affectee].unblock(*affected[affectee])
            self.state[affectee].update_heat()

        index = BOARD_KEY_INDEX[location]
        self.hashstate = self.hashstate[:index] + ' ' + self.hashstate[index+1:]
        self.all.remove(piece)
        if piece.color == 'w':
            self.white.remove(piece)
        else:
            self.black.remove(piece)
        # return set(affected)

    def relocate_piece(self, from_, to):
        if isinstance(from_, Piece):
            piece = from_
            # from_ = piece.location  ## altering value here, may also change it on a higher level if the obj is mutable
            origin = piece.location
        else:
            piece = self.state[from_]
            if not piece:
                message = 'Trying to move the air at ' + from_
                raise MoveException(message)
            origin = from_

        if self.state[to]:
            message = 'Are you blind - there is another piece at that spot: ' + repr(self.state[to])
            raise MoveException(message)

        origin_affected = self.find_unblockers(origin)
        piece.location = to
        self.state[to] = piece
        self.state[origin] = None
        piece.init_moves()
        to_affected = self.find_blockers(to)
        for affectee in origin_affected.keys():
            self.state[affectee].unblock(*origin_affected[affectee])
            self.state[affectee].update_heat()

        for affectee in to_affected:
            piece.block(*affectee)
            self.state[affectee[0]].block(to, neggate_direction(affectee[1]))
            self.state[affectee[0]].update_heat()

        index = BOARD_KEY_INDEX[to]
        self.hashstate = self.hashstate[:index] + piece.hashtype + self.hashstate[index+1:]
        index = BOARD_KEY_INDEX[origin]
        self.hashstate = self.hashstate[:index] + ' ' + self.hashstate[index+1:]
        piece.update_heat()      # the actor piece heat can be updated here

    def process_actions(self, actions):
        # common routine of the exec_move and undo_move
        for act in actions:
            getattr(self, act[0])(*act[1])

    undo_move = process_actions

    def execute_move(self, move):
        actions, undo = move.actions()
        self.process_actions(actions)
        undo.append(('set_incheck', [self.white_checked, self.black_checked]))
        self.update_incheck(move.piece.color)
        return undo

    def set_incheck(self, white_is_in_check, black_is_in_check):
        self.white_checked = white_is_in_check
        self.black_checked = black_is_in_check

    def update_incheck(self, color):
        if color == 'w':
            self.black_checked = self.is_in_check(self.black_king.location, 'w')
            if self.black_checked:
                self.checks = self.find_checkers(self.black_king.location, 'w')
            else:
                self.checks = []
            self.pinners = self.find_pinners(self.black_king.location, 'w')
        else:
            self.white_checked = self.is_in_check(self.white_king.location, 'b')
            if self.white_checked:
                self.checks = self.find_checkers(self.white_king.location, 'b')
            else:
                self.checks = []
            self.pinners = self.find_pinners(self.white_king.location, 'b')

    def prevalidate_move(self, move_piece, move):
        if move_piece.color == 'w':
            opposite_color = 'b'
            castle_row = '1'
            turns_king_location = self.white_king.location
            opponent_pieces = self.black
            turns_king_in_check = self.white_checked
        else:
            opposite_color = 'w'
            castle_row = '8'
            turns_king_location = self.black_king.location
            opponent_pieces = self.white
            turns_king_in_check = self.black_checked

        move_is_capture = move.type_ == 't' or move.type_ == 'e' or move.type_ == '+'

        if move_piece.type_ == 'k':
            # king's landing
            if self.is_in_check(move.destination, opposite_color):
                return False
            is_in_check = False
            if move.type_ == 'c':
                # king's origin
                if turns_king_in_check:
                    return False
                if move.notation.count('O') == 2:
                    jump_over = 'f' + castle_row
                else:
                    jump_over = 'd' + castle_row
                # jump over
                if self.is_in_check(jump_over, opposite_color):
                    return False
            return True
        else:   # not moving the king
            # consider discovery
            for pin in self.pinners:
                if move_piece == pin.pinnee and move.destination != pin.pinner.location and move.destination not in pin.pinner.paths[pin.direction].squares:
                    return False
            # consider covering check
            if turns_king_in_check:
                for check in self.checks:
                    if check.checker.paths:
                        if move.destination != check.checker.location and check.direction in check.checker.paths and move.destination not in check.checker.paths[check.direction].walk:
                            return False
                    else:
                        if move.destination != check.checker.location:
                            return False

            return True

    def is_in_check(self, location, by_color):
        return self.heat[by_color][location] != 0

    def find_blockers(self, location):
        blockers = []
        for d in ['N','E','S','W']:
            for i in range(len(INVERSE_HIT_MAP[location][d])):
                hitter = INVERSE_HIT_MAP[location][d][i]
                if self.state[hitter]:
                    blockers.append((hitter, d))
                    break

        for d in ['NE','SE','SW','NW']:
            for i in range(len(INVERSE_HIT_MAP[location][d])):
                hitter = INVERSE_HIT_MAP[location][d][i]
                if self.state[hitter]:
                    blockers.append((hitter, d))
                    break

        return blockers

    def find_unblockers(self, location):
        unblockers = {'SE': None, 'NE': None, 'W': None, 'SW': None, 'N': None, 'E': None, 'S': None, 'NW': None}

        for d in ['N','E','S','W']:
            for i in range(len(INVERSE_HIT_MAP[location][d])):
                hitter = INVERSE_HIT_MAP[location][d][i]
                if self.state[hitter]:
                    unblockers[d] = hitter
                    break

        for d in ['NE','SE','SW','NW']:
            for i in range(len(INVERSE_HIT_MAP[location][d])):
                hitter = INVERSE_HIT_MAP[location][d][i]
                if self.state[hitter]:
                    unblockers[d] = hitter
                    break

        results = {}
        for d in ['N','E','S','W', 'NE','SE','SW','NW']:
            if unblockers[d]:
                opposite = neggate_direction(d)
                if unblockers[opposite]:
                    results[unblockers[d]] = (location, opposite, unblockers[opposite])
                else:
                    results[unblockers[d]] = (location, opposite, None)
        return results

    def find_checkers(self, location, by_color):
        checkers = []
        for hitter in INVERSE_HIT_MAP[location]['knight']:
            if self.state[hitter] and self.state[hitter].designation == by_color+'n':
                checkers.append(Check(self.state[hitter], location))
                break

        if by_color == 'w':
            for hitter in INVERSE_HIT_MAP[location]['wpawn']:
                if self.state[hitter] and self.state[hitter].designation == 'wp':
                    checkers.append(Check(self.state[hitter], location))
                    break
        else:
            for hitter in INVERSE_HIT_MAP[location]['bpawn']:
                if self.state[hitter] and self.state[hitter].designation == 'bp':
                    checkers.append(Check(self.state[hitter], location))
                    break

        for hitter in INVERSE_HIT_MAP[location]['king']:
            if self.state[hitter] and self.state[hitter].designation == by_color+'k':
                checkers.append(Check(self.state[hitter], location))
                break

        for d in ['N','E','S','W']:
            for i in range(len(INVERSE_HIT_MAP[location][d])):
                hitter = INVERSE_HIT_MAP[location][d][i]
                if self.state[hitter]:
                    if self.state[hitter].designation == by_color+'q' or self.state[hitter].designation == by_color+'r':
                        checkers.append(Check(self.state[hitter], location, d))
                    break  # the direction is blocked if an enemy piece doesnt operate in that direction or own piece

        for d in ['NE','SE','SW','NW']:
            for i in range(len(INVERSE_HIT_MAP[location][d])):
                hitter = INVERSE_HIT_MAP[location][d][i]
                if self.state[hitter]:
                    if self.state[hitter].designation == by_color+'q' or self.state[hitter].designation == by_color+'b':
                        checkers.append(Check(self.state[hitter], location, d))
                    break  # the direction is blocked if an enemy piece doesnt operate in that direction or own piece

        return checkers

    def find_pinners(self, location, by_color):
        if by_color == 'w':
            own_color = 'b'
        else:
            own_color = 'w'
        pinners = []

        for d in ['N','E','S','W']:
            own_in_path_flag = None
            for i in range(len(INVERSE_HIT_MAP[location][d])):
                hitter = INVERSE_HIT_MAP[location][d][i]
                if self.state[hitter]:
                    if own_in_path_flag:
                        if self.state[hitter].designation == by_color+'q' or self.state[hitter].designation == by_color+'r':
                            pinners.append(Pin(self.state[hitter], own_in_path_flag, location, d))
                        break       # pin captured
                    else:
                        if self.state[hitter].designation[0] == own_color:
                            own_in_path_flag = self.state[hitter]
                        else:
                            break   # opponent piece encountered first

        for d in ['NE','SE','SW','NW']:
            own_in_path_flag = None
            for i in range(len(INVERSE_HIT_MAP[location][d])):
                hitter = INVERSE_HIT_MAP[location][d][i]
                if self.state[hitter]:
                    if own_in_path_flag:
                        if self.state[hitter].designation == by_color+'q' or self.state[hitter].designation == by_color+'b':
                            pinners.append(Pin(self.state[hitter], own_in_path_flag, location, d))
                        break       # pin captured
                    else:
                        if self.state[hitter].designation[0] == own_color:
                            own_in_path_flag = self.state[hitter]
                        else:
                            break   # opponent piece encountered first
        return pinners
