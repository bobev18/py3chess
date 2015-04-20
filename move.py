class MoveException(Exception):
    def __init__(self, *args):
        # *args is used to get a list of the parameters passed
        self.args = [a for a in args]

class Move():

	def __init__(self, piece, type_, destination, notation, promote_to = None):
		self.piece = piece
		self.origin = piece.location
		self.type_ = type_
		self.destination = destination
		self.notation = notation
		self.promote_to = promote_to

	def __repr__(self):
		return self.notation