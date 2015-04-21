class MoveException(Exception):
    def __init__(self, *args):
        # *args is used to get a list of the parameters passed
        self.args = [a for a in args]

class Move():

    def __init__(self, piece, type_, destination, notation, extra = None):
        self.piece = piece
        self.origin = piece.location
        self.type_ = type_
        self.destination = destination
        self.notation = notation
        self.promote_to = ''
        self.taken = None
        self.catsling_rook = None
        if type_ == 'p':
            self.promote_to = extra
        if type_ == '+':
            self.promote_to = extra[0]
            self.taken = extra[1]
        if type_ == 't' or type_ == 'e':
            self.taken = extra
        if type_ == 'c':
            self.catsling_rook = extra

    def __repr__(self):
        return self.notation

    def actions(self):
        actions=[]
        undo=[]
        if self.type_=='m' or self.type_ == 'm2' or self.type_ == 'mk':
            actions.append(['relocate', self.piece, self.destination])
            undo.append(['relocate', self.destination, self.piece.location])
        elif self.type_=='t' or self.type_=='e':
            actions.append(['remove', self.taken])
            actions.append(['relocate', self.piece, self.destination])
            undo.append(['relocate', self.destination, self.piece.location])
            undo.append(['add', self.taken])
        elif self.type_=='p':
            actions.append(['add', self.piece.col, self.promote_to.lower(), self.destination])
            actions.append(['remove', self.piece])
            undo.append(['add', self.piece])
            undo.append(['remove', self.destination])
        elif self.type_=='+':
            actions.append(['remove', self.taken])
            actions.append(['add', self.piece.col, self.promote_to.lower(), self.destination])
            actions.append(['remove', self.piece])
            undo.append(['add', self.piece])
            undo.append(['remove', self.destination])
            undo.append(['add', self.taken])
        elif self.type_ == 'c':
            if self.notation == 'O-O':
                actions.append(['relocate', self.catsling_rook, 'f'+self.piece.location[1]])
                actions.append(['relocate', self.piece, self.destination])
                undo.append(['relocate', self.destination, self.piece.location])
                undo.append(['relocate', self.catsling_rook, 'h'+self.piece.location[1]])
            else: #O-O-O
                actions.append(['relocate', self.catsling_rook, 'd'+self.piece.location[1]])
                actions.append(['relocate', self.piece, self.destination])
                undo.append(['relocate', self.destination, self.piece.location])
                undo.append(['relocate', self.catsling_rook, 'a'+self.piece.location[1]])

        return actions, undo