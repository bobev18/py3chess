class MoveException(Exception):
    def __init__(self, *args):
        # *args is used to get a list of the parameters passed
        self.args = [a for a in args]

class Move():

	def __init__(self, piece, origin, type_, destination, notation):
		if piece.location == origin:
			self.piece = piece
		else:
			message = "piece " + str(piece) + " location does not match the origin " + origin
			raise MoveException(message)

		self.origin = origin
		self.type_ = type_
		self.destination = destination
		self.notation = notation

	def __repr__(self):
		return self.notation