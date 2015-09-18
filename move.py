class Move():
    def __init__(self, piece, type_, destination, notation, extra=None):
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
        actions = []
        undo = []

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
                actions.append({'act':'relocate_piece', 'args':[self.catsling_rook, 'f'+self.piece.location[1]]})
                actions.append({'act':'relocate_piece', 'args':[self.piece, self.destination]})
                undo.append({'act':'relocate_piece', 'args':[self.destination, self.piece.location]})
                undo.append({'act':'relocate_piece', 'args':[self.catsling_rook, 'h'+self.piece.location[1]]})
            else:  # O-O-O
                actions.append({'act':'relocate_piece', 'args':[self.catsling_rook, 'd'+self.piece.location[1]]})
                actions.append({'act':'relocate_piece', 'args':[self.piece, self.destination]})
                undo.append({'act':'relocate_piece', 'args':[self.destination, self.piece.location]})
                undo.append({'act':'relocate_piece', 'args':[self.catsling_rook, 'a'+self.piece.location[1]]})

        return actions, undo

    def flat_actions(self):
        actions = []
        undo = []

        if self.type_ == 'm' or self.type_ == 'm2' or self.type_ == 'mk':
            actions = [('relocate_piece', [self.origin, self.destination])]
            undo = [('relocate_piece', [self.destination, self.origin])]
        elif self.type_ == 't' or self.type_ == 'e':
            actions = [('remove_piece', [self.taken.location]),
                       ('relocate_piece', [self.origin, self.destination])]
            undo = [('relocate_piece', [self.destination, self.origin]),
                    ('add_piece', [self.taken.designation+'@'+self.taken.location])]
        elif self.type_ == 'p':
            actions = [('add_piece', [self.piece.color, self.promote_to.lower(), self.destination]),
                       ('remove_piece', [self.origin])]
            undo = [('add_piece', [self.piece.designation+'@'+self.piece.location]),
                    ('remove_piece', [self.destination])]
        elif self.type_ == '+':
            actions = [('remove_piece', [self.taken.location]),
                       ('add_piece', [self.piece.color, self.promote_to.lower(), self.destination]),
                       ('remove_piece',[self.origin])]
            undo = [('add_piece', [self.piece.designation+'@'+self.piece.location]),
                    ('remove_piece', [self.destination]),
                    ('add_piece', [self.taken.designation+'@'+self.taken.location])]
        elif self.type_ == 'c':
            if self.notation == 'O-O':
                actions = [('relocate_piece', [self.catsling_rook.location, 'f'+self.origin[1]]),
                           ('relocate_piece', [self.origin, self.destination])]
                undo = [('relocate_piece', [self.destination, self.origin]),
                        ('relocate_piece', ['f'+self.origin[1], 'h'+self.origin[1]])]
            else:  # O-O-O
                actions = [('relocate_piece', [self.catsling_rook.location, 'd'+self.origin[1]]),
                           ('relocate_piece', [self.origin, self.destination])]
                undo = [('relocate_piece', [self.destination, self.origin]),
                        ('relocate_piece', ['d'+self.origin[1], 'a'+self.origin[1]])]

        return actions, undo

    def __eq__(self, other):
        if isinstance(other, self.__class__) \
        and self.piece == other.piece \
        and self.origin == other.origin \
        and self.type_[0] == other.type_[0] \
        and self.destination == other.destination \
        and str(self.promote_to) == str(other.promote_to) \
        and str(self.taken) == str(other.taken) \
        and str(self.catsling_rook) == str(other.catsling_rook):
            return True
        else:
            return False
        # and self.notation == other.notation \  ----   this can be added after 'generating disambiguated notation' is implemented onto the generic naive move results
