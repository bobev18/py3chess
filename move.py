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
        # if self.notation == 'O-O':
        #     print('type', self.type_)

        if self.type_ == 'm' or self.type_ == 'm2' or self.type_ == 'mk':
            actions.append({'act':'relocate_piece', 'args':[self.piece, self.destination]})
            undo.append({'act':'relocate_piece', 'args':[self.destination, self.piece.location]})
        elif self.type_ == 't' or self.type_ == 'e':
            actions.append({'act':'remove_piece', 'args':[self.taken]})
            actions.append({'act':'relocate_piece', 'args':[self.piece, self.destination]})
            undo.append({'act':'relocate_piece', 'args':[self.destination, self.piece.location]})
            undo.append({'act':'add_piece', 'args':[self.taken]})
        elif self.type_ == 'p':
            actions.append({'act':'add_piece', 'args':[self.piece.color, self.promote_to.lower(), self.destination]})
            actions.append({'act':'remove_piece', 'args':[self.piece]})
            undo.append({'act':'add_piece', 'args':[self.piece]})
            undo.append({'act':'remove_piece', 'args':[self.destination]})
        elif self.type_ == '+':
            actions.append({'act':'remove_piece', 'args':[self.taken]})
            actions.append({'act':'add_piece', 'args':[self.piece.color, self.promote_to.lower(), self.destination]})
            actions.append({'act':'remove_piece', 'args':[self.piece]})
            undo.append({'act':'add_piece', 'args':[self.piece]})
            undo.append({'act':'remove_piece', 'args':[self.destination]})
            undo.append({'act':'add_piece', 'args':[self.taken]})
        elif self.type_ == 'c':
            if self.notation == 'O-O':
                print('entered in OO')
                actions.append({'act':'relocate_piece', 'args':[self.catsling_rook, 'f'+self.piece.location[1]]})
                actions.append({'act':'relocate_piece', 'args':[self.piece, self.destination]})
                undo.append({'act':'relocate_piece', 'args':[self.destination, self.piece.location]})
                undo.append({'act':'relocate_piece', 'args':[self.catsling_rook, 'h'+self.piece.location[1]]})
            else: #O-O-O
                actions.append({'act':'relocate_piece', 'args':[self.catsling_rook, 'd'+self.piece.location[1]]})
                actions.append({'act':'relocate_piece', 'args':[self.piece, self.destination]})
                undo.append({'act':'relocate_piece', 'args':[self.destination, self.piece.location]})
                undo.append({'act':'relocate_piece', 'args':[self.catsling_rook, 'a'+self.piece.location[1]]})

        if self.notation == 'O-O':
            print('actions/undo', actions, undo)


        return actions, undo