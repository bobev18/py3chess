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
            actions.append(('relocate_piece', [self.piece, self.destination]))
            undo.append(('relocate_piece', [self.destination, self.piece.location]))
        elif self.type_ == 't' or self.type_ == 'e':
            actions.append(('remove_piece', [self.taken]))
            actions.append(('relocate_piece', [self.piece, self.destination]))
            undo.append(('relocate_piece', [self.destination, self.piece.location]))
            undo.append(('add_piece', [self.taken]))
        elif self.type_ == 'p':
            actions.append(('add_piece', [self.piece.color, self.promote_to.lower(), self.destination]))
            actions.append(('remove_piece', [self.piece]))
            undo.append(('add_piece', [self.piece]))
            undo.append(('remove_piece', [self.destination]))
        elif self.type_ == '+':
            actions.append(('remove_piece', [self.taken]))
            actions.append(('add_piece', [self.piece.color, self.promote_to.lower(), self.destination]))
            actions.append(('remove_piece', [self.piece]))
            undo.append(('add_piece', [self.piece]))
            undo.append(('remove_piece', [self.destination]))
            undo.append(('add_piece', [self.taken]))
        elif self.type_ == 'c':
            if self.notation == 'O-O':
                actions.append(('relocate_piece', [self.catsling_rook, 'f'+self.piece.location[1]]))
                actions.append(('relocate_piece', [self.piece, self.destination]))
                undo.append(('relocate_piece', [self.destination, self.piece.location]))
                undo.append(('relocate_piece', [self.catsling_rook, 'h'+self.piece.location[1]]))
            else:  # O-O-O
                actions.append(('relocate_piece', [self.catsling_rook, 'd'+self.piece.location[1]]))
                actions.append(('relocate_piece', [self.piece, self.destination]))
                undo.append(('relocate_piece', [self.destination, self.piece.location]))
                undo.append(('relocate_piece', [self.catsling_rook, 'a'+self.piece.location[1]]))

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
