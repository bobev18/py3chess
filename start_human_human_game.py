from game import Game

# game = Game()
# game = Game(board_position={'e2':'  ','c8':'  ','e1':'  ','b6':'  ','e8':'bk','e7':'  ','g5':'  ','b1':'  ','a2':'  ','g6':'  ','e6':'  ','f6':'  ','h4':'  ','h7':'bp','g1':'wk','a5':'wp','b2':'  ','d3':'wp','c1':'  ','e3':'  ','c4':'  ','a6':'bp','a4':'  ','d8':'  ','f3':'wp','a8':'br','d2':'  ','c6':'  ','c7':'bp','g8':'  ','d1':'wq','f2':'wp','f1':'wr','g3':'  ','g2':'  ','b8':'  ','c2':'wp','f8':'  ','b4':'bq','b7':'bp','f5':'  ','f4':'  ','d4':'bp','h3':'wp','a3':'  ','c3':'  ','b3':'  ','d7':'  ','b5':'  ','e4':'wn','h6':'  ','d5':'  ','h2':'  ','h8':'br','a1':'wr','h1':'  ','g4':'  ','g7':'bp','h5':'  ','c5':'  ','a7':'bb','f7':'bp','e5':'  ','d6':'  '})
game = Game(board_position={'c8':'  ','a2':'  ','f3':'wp','g7':'bp','b3':'  ','a1':'wr','h6':'  ','f1':'  ','e2':'  ','h4':'  ','c7':'bp','h8':'  ','b4':'  ','c2':'wp','h5':'  ','d4':'bp','d1':'  ','d3':'wp','d6':'  ','c1':'  ','d5':'  ','b8':'  ','h1':'  ','g5':'  ','c3':'  ','c6':'  ','g4':'  ','e6':'  ','c5':'  ','a7':'bb','f7':'bp','a8':'br','f8':'br','h3':'wp','e4':'wn','f6':'  ','a5':'wp','f2':'wp','g8':'bk','b1':'  ','a4':'  ','b7':'bp','g2':'  ','d2':'  ','d8':'  ','a3':'  ','b6':'  ','g6':'  ','g3':'  ','f4':'  ','g1':'wk','f5':'  ','e1':'wr','b2':'  ','e5':'  ','e8':'  ','d7':'  ','a6':'bp','h2':'  ','c4':'  ','b5':'  ','e7':'  ','e3':'  ','h7':'bp'})
try:
    game.start()
except:
    print('notation:')
    print(game.full_notation)
    print('\nend position:')
    print(game.board.export())
    print('white moves:', [ z for z in game.history if z.piece.color == 'w' ])
    print('black moves:', [ z for z in game.history if z.piece.color == 'b' ])
    raise
