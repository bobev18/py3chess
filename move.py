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
        # DDRRAAI with R & I having 2 args, and the rest 1 arg, so [D1, D2, R1a, R1b, R2a, R2b, A1, A2, Ia, Ib]
        if self.type_ == 'm' or self.type_ == 'm2' or self.type_ == 'mk':
            actions = [None, None, self.origin, self.destination, None, None, None, None, None, None]
            undo = [None, None, self.destination, self.origin, None, None, None, None, None, None]
        elif self.type_ == 't' or self.type_ == 'e':
            actions = [self.taken.location, None, self.origin, self.destination, None, None, None, None, None, None]
            undo = [None, None, None, None, self.destination, self.origin, self.taken.designation+'@'+self.taken.location, None, None, None]
        elif self.type_ == 'p':
            actions = [self.origin, None, None, None, None, None, self.promote_to.designation+'@'+self.destination, None, None, None]
            undo = [self.destination, None, None, None, None, None, self.piece.designation+'@'+self.origin, None, None, None]
        elif self.type_ == '+':
            actions = [self.origin, self.taken.location, None, None, None, None, self.promote_to.designation+'@'+self.destination, None, None, None]
            undo = [self.destination, None, None, None, None, None, self.piece.designation+'@'+self.origin, self.taken.designation+'@'+self.taken.location, None, None]
        elif self.type_ == 'c':
            if self.notation == 'O-O':
                actions = [None, None, self.catsling_rook.location, 'f'+self.origin[1], self.origin, self.destination, None, None, None, None]
                undo = [None, None, self.destination, self.origin, 'f'+self.origin[1], self.catsling_rook.location, None, None, None, None]
            else:  # O-O-O
                actions = [None, None, self.catsling_rook.location, 'd'+self.origin[1], self.origin, self.destination, None, None, None, None]
                undo = [None, None, self.destination, self.origin, 'd'+self.origin[1], self.catsling_rook.location, None, None, None, None]

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
