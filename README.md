py3chess
===========

Chess engine featuring move validation and stupid AI
####################################################

Move validation against check discovery and moving king into chekced field, requires the move to be executed, because:
 |  |  |  |  |bk|  |  |  |
 |  |  |  |  |  |  |  |  |
 |  |  |  |  |  |  |  |  |
 |  |  |  |  |bq|  |  |  |
 |  |  |  |  |wr|  |  |  |
 |  |  |bn|  |  |  |  |  |
 |  |  |  |  |  |  |  |  |
 |  |  |  |  |wk|  |  |  |

naive moves for wr@e4 are [Rxe5, Rf4, Rg4, Rh4, Re3, Re2, Rd4, Rc4, Rb4, Ra4]
the valid moves are [Rxe5, Re3, Re2]
the way discover_check works, is:
 1. take the king's position(e1) and the move origin (e4) and determine direction along which we need to seek check discovery
 2. take from INVERSE_HIT_MAP locations of potential hitters for the king's square - INVERSE_HIT_MAP['e4'][direction]
 3. iterate the returned locations (which are in order), and check via board state, if there is a piece
  3.1. if the piece is relevant - opposite color, QR along lines, and QB along diagonals - it returns that move leads to check discovery
  3.2. if the piece is irrelevant - it returns that there is NO check discovery
 4. if iteration ends without any piece alon the direction - it returns that there is NO check discovery

This will only work properly if the the new location for Re3, Re2, is reflected onto the board state i.e. the move is executed
There are couple of alterations that may be saved:
  - change of lists of pieces - whites, blacks
  - change relocation piece selfawareness -- is_in_check uses only piece.designation, so outdated attributes as location, x & y will not affect it's work.


