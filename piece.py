class Piece():
	def __init__(self, color, type_, location):
		self.color = color
		self.type_ = type_
		self.location = location

	def __repr__(self):
		return self.color + self.type_ + '@' + self.location

