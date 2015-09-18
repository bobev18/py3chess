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
Furthermore we want to evaluate the cutoff position not only via heuristic but whether the it's mate/stalemate; the mate/stalemate evaluation, requires generating all valid moves for the position reached. That means that cutting off at semi-move 13, will need to evaluate position resulting of executing move 13. That evaluation includes validating all moves available at this position, which is achieved via executing them i.e. to fully evaluate move 13, we need to execute all posible depth 14 moves;
If we generate the new lvl 14 nodes during evaluation of a lvl 13 move, and we have to execute lvl 14 moves to check for mate/stalemate, there is no case of a node with expansions for naive moves; should not create nodes for lvl 14 at the time of evaluating cutoff=13

every node needs to pass gamestate check, because game can hit mate/stalemate in the nodes between root and cutoff


The mem usage for cutoff node @ depth 3 is about 1KB per avaible subsequent move i.e 
cutoff subnodes    : 28
cutoff subnodes mem: 26056 bytes
Evaluating to depth 3, actualy expands and creates depth 4, and the total number of nodes is the vicinity of 666838, which on 64bit system took about 450MB. If going to next level adds 30 nodes on average, we are looking at ~15GB mem usage, which is crazy.
The nodes should be shrunk! How are the nodes to be reused when next move is to be generated? Due to the opponent move, we will be expanding from a node that is on a node of depth 2 in the existing tree. We will need to carry out the entire recursion anyway to properly compare all position at the new depth. The cost that could be saved is determining expansions and validating the moves in corresponding to nodes in the current tree. The cost of the nodes is in great part storeing the Move objects, which contain at least one Piece object. The core of the Move is ability to provide "actions" which are instructions for executing a move. They make calls to add_piece, relocate_piece, remove_piece with the relevant arguments:
```
	actions [ {'act':'remove_piece', 'args':[self.taken]},
    	      {'act':'relocate_piece', 'args':[self.piece, self.destination]}, ]
```
in paralel the undo actions are produced:
```
	undo    [ {'act':'relocate_piece', 'args':[self.destination, self.piece.location]},
    	      {'act':'add_piece', 'args':[self.taken]}, ]
```
These constructs rely on Piece objects stored in the Move, however the methods add_piece, relocate_piece, remove_piece also suport arguments in the form of strings indicating positions in the board.state.
If a method that generates actions and undo with string params is implemented, the Nodes could store only that information instead the entire Move object

Changed the structure of the actions structure:
```
	actions = [('remove_piece', [self.taken.location]),
               ('relocate_piece', [self.origin, self.destination])]
    undo = [('relocate_piece', [self.destination, self.origin]),
            ('add_piece', [self.taken.designation+'@'+self.taken.location])]
```
Because of that, and because no validation will be required during execution, the methods execute_move, process_actions and undo_actions - should have an alternative implementation utilizing the "flat" actions structure