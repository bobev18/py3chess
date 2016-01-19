py3chess
===========

Chess engine featuring move validation and stupid AI
####################################################

Move validation against check discovery and moving king into chekced field, requires the move to be executed, because:
```
 |  |  |  |  |bk|  |  |  |
 |  |  |  |  |  |  |  |  |
 |  |  |  |  |  |  |  |  |
 |  |  |  |  |bq|  |  |  |
 |  |  |  |  |wr|  |  |  |
 |  |  |bn|  |  |  |  |  |
 |  |  |  |  |  |  |  |  |
 |  |  |  |  |wk|  |  |  |
```
naive moves for wr@e4 are: [Rxe5, Rf4, Rg4, Rh4, Re3, Re2, Rd4, Rc4, Rb4, Ra4]
the valid moves are [Rxe5, Re3, Re2].
The way discover_check works, is:
1. execute the move
2. take the king's position(e1) and the move origin (e4) and determine direction along which we need to seek check discovery
3. take from INVERSE_HIT_MAP locations of potential hitters for the king's square and the direction - INVERSE_HIT_MAP['e1'][direction]
4. iterate the returned locations (which are ordered along the direction), and check via board state, if there is a piece
4.1. if the piece is relevant - opposite color, Q/R along lines, and Q/B along diagonals - it returns True i.e. that move leads to check discovery
4.2. if the piece is irrelevant - it returns False i.e. that there is NO check discovery
5. if iteration ends without finding any piece along the direction - it returns False i.e. that there is NO check discovery
This will only work properly if the moves Re3, Re2, have the rook's new location reflected onto the board state i.e. the move is executed

The execution of the move being validated, could be somewhat different from the complete "in game" execution. There are couple actions of the "full" execution that could be omitted:
  * (1) change of lists of pieces - whites, blacks -- these are not used for check validations
  * (2) change Piece instance attributes to reflect the relocation
    * `discover_check` does not use piece object at all
    * `is_in_check` uses only piece.designation, so outdated attributes as location, x & y will not affect it's work
Item (1) is carried out in add_piece and in remove_piece;
Item (2) is carried out, as it's integrated into relocate_piece; relocate_piece is the only action that requires Piece attributes update

The current implementation has the check level validations integrated in the move execution method. The history dependent checks - castling and stalemate by repetition - should be in the Game class. Disambiguation should also be in the Game class.

Migrated the conditional checks:

	if new_piece.type_ == 'k':
        self.white_king = new_piece

    if new_piece.type_ == 'k':
        self.black_king = new_piece

from add_piece to spawn_pieces, as this is the only situation where this may occur, while add_piece is called from few more places

Having all valid moves upfront a human move (instead of all naive moves + validation at execution) is needed, because input notation is compared to these moves. If we compare against naive moves, we may accept prompt, then fail validation during execution. That would entail returning to prompt, but that's not an option in terms of cycle structure.

Validating moves takes executing them, one way or another. For AI we need to execute many moves anyway (for evaluation), so it's efficient to complete the validation as part of the evaluation. As AI evaluates & validates moves of the opponent, these results should be kept and reused. If such record is not available and validating human player moves is needed, it requires only depth of 1 of all naive moves, so it's good to have that as a single method.


I feel that cross knowledge between classes is not a good practice, but I think I'll need to do it this time:
class Game has objects of Player class, and I need the instance of Player object to know of a instance of Game; I can pass the Game's self as parameter to the Player constructor. It feels it may be better to implement sort of communication (using methods to pass data) between these classes instead of direct referencing, but I cant pinpoint why.

The question for the AI is as follows:
  When exploring moves, should there be:
  1. one boardset - just move pieces back and forth
  2. multiple boardsets - new board is spawned by copy from the old one, and one forward move is applied.
Option (2) is more demanding on memory, and, generally, reducing execution time comes at the cost of more memory. However it may turn out that making a copy of the board takes more time than processing undo - here's why:
a) Board class has an attribute that is a dict of instances of Piece objects. Simple board.copy() will create new variables for the attributes, but the new dict, will still refer to the same instances of the Piece objects. So a custom copy process needs to be implemented that creates copies of the Piece objects along with the other Board attributes. That will take execution time.
b) The exploration of the chess-tree is depth first - there will not be a need to switch between nodes that are not linked by single move (either execute_move to go a level deeper, or undo to go a level up).
On the other hand, option (2) could be easier for refactoring into a multi-threaded solution

Ultimately only a direct comparison of execution times will tell for sure which option is better.
Actually the copy needs to be of the Game instance, otherwise we cannot validate history dependent moves. Or implement compatible method in the AI class.

evaluating a move will always need to make full traversal - from the move node to all cutoff nodes, because the move score is not only dependent on the evaluation score of all cutoff nodes, but on comparison of scores on the intermediate nodes. In that regard, there will be no difference between evaluating a naive node, and one that has been verified.
Furthermore we want to evaluate the cutoff position not only via heuristic but whether the it's mate/stalemate; the mate/stalemate evaluation, requires generating all valid moves for the position reached. That means that cutting off at semi-move 13, will need to evaluate position resulting of executing move 13. That evaluation includes validating all moves available at this position, which is achieved via executing them i.e. to fully evaluate move 13, we need to execute all possible depth 14 moves;
If we generate the new lvl 14 nodes during evaluation of a lvl 13 move, and we have to execute lvl 14 moves to check for mate/stalemate, there is no case of a node with expansions for naive moves; should not create nodes for lvl 14 at the time of evaluating cutoff=13

every node needs to pass game state check, because game can hit mate/stalemate in the nodes between root and cutoff


The mem usage for cutoff node @ depth 3 is about 1KB per available subsequent move i.e
cutoff subnodes    : 28
cutoff subnodes mem: 26056 bytes
Evaluating to depth 3, actually expands and creates depth 4, and the total number of nodes is the vicinity of 666838, which on 64bit system took about 450MB. If going to next level adds 30 nodes on average, we are looking at ~15GB mem usage, which is crazy.
The nodes should be shrunk! How are the nodes to be reused when next move is to be generated? Due to the opponent move, we will be expanding from a node that is on a node of depth 2 in the existing tree. We will need to carry out the entire recursion anyway to properly compare all position at the new depth. The cost that could be saved is determining expansions and validating the moves in corresponding to nodes in the current tree. The cost of the nodes is in great part storing the Move objects, which contain at least one Piece object. The core of the Move is ability to provide "actions" which are instructions for executing a move. They make calls to add_piece, relocate_piece, remove_piece with the relevant arguments:
```
	actions [ {'act':'remove_piece', 'args':[self.taken]},
    	      {'act':'relocate_piece', 'args':[self.piece, self.destination]}, ]
```
in parallel the undo actions are produced:
```
	undo    [ {'act':'relocate_piece', 'args':[self.destination, self.piece.location]},
    	      {'act':'add_piece', 'args':[self.taken]}, ]
```
These constructs rely on Piece objects stored in the Move, however the methods add_piece, relocate_piece, remove_piece also support arguments in the form of strings indicating positions in the board.state.
If a method that generates actions and undo with string params is implemented, the Nodes could store only that information instead the entire Move object

Changed the structure of the actions structure:
```
	actions = [('remove_piece', [self.taken.location]),
               ('relocate_piece', [self.origin, self.destination])]
    undo = [('relocate_piece', [self.destination, self.origin]),
            ('add_piece', [self.taken.designation+'@'+self.taken.location])]
```
Because of that, and because no validation will be required during execution, the methods execute_move, process_actions and undo_actions - should have an alternative implementation utilizing the "flat" actions structure
However 1. determine_game_state pulls moves from Board.naive_moves, which are of type Move. 2. pre-defined moves from the chesstree, which would be flat type, so this will result in mixing flat and non flat execute_move methods. This can be resolved in 2 ways:
 a) make duplicate determine_game_state, that provides flat instead of Move type
 b) make a check within execute_move method, which of the two types of data is provided, and process accordingly

Actually there is c) that uses determine_game_state to pull type Move, but uses Move.flat_actions() to save in the Node
NOTE:
 With using flat_execute moves, there are few tasks to be done alongside the method call:
  - the method returns 'data' to be appended to the undo_actions
  - the `board.white_checked` & `board.black_checked` should be updated by `board.update_incheck_variable_state(<turning color>)`
  - both execute and undo processes call the same `process_flat_actions` method


game.history takes Moves, and info from Nodes has only move_actions !!!  => the gamestate check will error. Options:
  XXXa) flatten historyXXX - wont work, because hist check relies on move.type_ for the e.p moves
 b) new flat format
 c) rework history to contain be individual variables for each of the 4 castling moves, and just the prior move for the en passant
   - this may be tricky for handling undo


Possible bugs :
1. original `validate_against_history` uses `return len(nullifying_moves) == 0` which means moving either rook invalidates both castling moves
2. node.optimum is based on node.color, but is actually used to compare evaluations of instance node.subnodes ==> needs to be inversed
3. ai.expand_node should handle mate/stalemate results of the gamestate check and set the local_optimum default value (which later passes to the node.score)
4. got test that went Nd6, Kf8, ??  -- response to Nd6 should be cxd6
   - turned out same as (3) - had "fixed" the optimum under `evaluate_position`, instead of under Node

The switch of the history validation to utilize `special_moves` instead of `history` attribute still left move as argument of the record_history which beats the purpose of the change. The record_history needs to operate with flat_actions as input argument :(


noticed that python process hit 872 MB mem use (in task manager) while final size for root node reached 468 MB

going to depth 4 is absurd - mem usage hit over 20GB
I think the previous depth 4 results were captured without having the check gamestate create depth 5 nodes without evaluating them
I could probably reduce the tree, by keeping only the best candidate depth 1 branch. Since AI cant choose non optimal score, an inferior branch can be cut.
On deeper branches we cannot cut oponent branches, but on any own branches we can apply the same strategy. No, because the optimum will change due to deeper lvl evaluataions.


##### Concept to discard Move obj, and replace it with a list ===

The way undo_actions get the 'data' for the w_in_check/b_in_check position, the same should be added to the move_actions before undo is processed. This should allow conditioning the calls to `update_incheck_variable_state` which relies on `is_in_check`, to avoid the call id the 'data' is present in the move_actions
MMM the first execution is done based on result from move.actions while the 2nd is from move.flat_actions so values from the 1st cannot be transfered in the 2nd. To make it work we'll need global use of flat actions and retaining them from the gamestate moves to the <expand> moves

the plan is to:
1. update the original board methods to simplify structure
2. revert the chessboard to use non-flat moves === Move objects
3. make a flat branch and implement only the flat moves
4. make direct comparison between flat and non flat mem usage

**Results are: storing Move obj is better than a flat list !!!!!!!**

*Note: tottime - is time spend in the method minus the sub calls*

##### Concept to merge directional cycles

Have to find another way to optimize is_in_check:
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   571117   11.666    0.000   12.110    0.000 board.py:388(is_in_check)

merged directional cycles
   549840   15.223    0.000   16.116    0.000 board.py:388(is_in_check)

**Result: There is no point of altering the cycles -- the number of comparisons between hitters and board state cannot be reduced**


##### Heat Concept

The timing of the results indicate about 200sec out of 800sec are in `board.is_in_check`. Instead of checking potential hitters, a heat map could be used. The heated nodes are the destinations in the naive expansions up to a blockage;
  Moving one piece can influence the naive expansions of another piece that is not involved in the move. This will require recalculating all naives for all pieces. This work (naives for each piece) is actually done in the non-heat implementation. The difference is in the order. The non-heat order is:
    loop pieces in `detemine_agmaestate` -> for each piece call `valid_moves_at`, which `board.naive_moves` i.e **recalculates** the naive moves for the piece -> loops over moves and for each move does -> execute -> validate for discover_/is_in_ check -> undo ===> next move ===> next piece
  Finding all naives for a position before proceeding to validation process will require two separate cycles through pieces:
    cycle opponent pieces and call `board.naive_moves` to generate the heat map
    cycle through own pieces and pass the validation where is_in_check reads the heat map instead of INVERSE_HIT_MAP
^^^^
the above is structural change to many modules/classes, and needs to be carried in new branch stemming from master!!!!

**Preliminary Result: heat map works twice slower than the current is_in_check!**
(This preliminary had a bug, see further down for the ?final? result)

To avoid the verifying all potential hitter positions is to keep track of these during the move executions. That information cannot be the validated moves but it should work for naive moves
This is more core change than the heat map

High level concept is like this:
keep Piece's own equivalent of ACT_MAP and update it dynamically based on move executions
let's have a method "update_naives"; for non directional moves, that will be an if check, but for directional ones it will be a cutoff for the direction sequence
so after move execution we cycle through pieces, and call update_naives with the Move (or destination, etc)
To avoid another cycle, the updated data should be passed into heatmap
--- initial naive_moves for a piece need to be processed via the current naive_moves method
!!! also for newly created pieces (pawn promos), the initial state also needs to be done via the current method !!!

Added embedded inner ifs for un/block methods in Path.
Moved heat accumulation to single separate cycle in the end of process_actions
Added sorting of subnodes in chesstree to ensure consistency of move considerations for the cProfile tests

Using piece.raw_moves is a bug, because that is not updated after change in piece.location
BUG: currently  `others` relies on `raw_moves` -- should add test
Maybe not a bug - added test, and it passes without changes to the use of raw_moves
Well, turns out that board.relocate calls piece.init_moves(), which updates raw_moves == FIXED

BUG: using conditioned block for the consideration calls to un/block in the last commit fails to allow moves alongside pinned line
FIXED in pinners cycle

BUG: the AI has deteriorated:

      |br|  |  |  |bk|  |  |br|
      |bb|bp|bp|  |  |bp|bp|bp|
      |bp|  |  |  |  |  |  |  |
      |wp|  |  |  |  |  |  |  |
      |  |bq|  |bp|wn|  |  |  |
      |  |  |  |wp|  |wp|  |wp|
      |  |  |wp|  |  |wp|  |  |
      |wr|  |  |wq|  |wr|wk|  |

      optimal move with score 0 and move path: ||Nd6|Kd7|Nxb7,

because the checker'n'pinners fails to accommodate case where checker is captured by another piece
FIXED by adding `if move.destination != piece.location:` in the checkers loop

