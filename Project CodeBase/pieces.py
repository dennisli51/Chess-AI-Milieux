#Image photos taken from 
#https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent

#Defines the classes for all chess pieces
class Piece(object): 
    def __init__(self, color):
        self.color = color
        self.image = ''
    
    def getImage(self):
        return self.image

    def getColor(self):
        return self.color

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 100
        if self.color == 'black':
            self.image = 'Black Pawn.png'
        elif self.color == 'white': 
            self.image = 'White Pawn.png'    
    
    def getType(self):
        return "pawn"

    def getValue(self): 
        return self.value

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 330
        if self.color == 'black':
            self.image = 'Black Bishop.png'
        elif self.color == 'white': 
            self.image = 'White Bishop.png'
    def getType(self):
        return "bishop"

    def getValue(self): 
        return self.value

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 320
        if self.color == 'black':
            self.image = 'Black Knight.png'
        elif self.color == 'white': 
            self.image = 'White Knight.png'
    def getType(self):
        return "knight"

    def getValue(self): 
        return self.value

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 500
        if self.color == 'black':
            self.image = 'Black Rook.png'
        elif self.color == 'white': 
            self.image = 'White Rook.png'
    def getType(self):
        return "rook"

    def getValue(self): 
        return self.value

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 900
        if self.color == 'black':
            self.image = 'Black Queen.png'
        elif self.color == 'white': 
            self.image = 'White Queen.png'
    def getType(self):
        return "queen"

    def getValue(self): 
        return self.value

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 10000
        if self.color == 'black':
            self.image = 'Black King.png'
        elif self.color == 'white': 
            self.image = 'White King.png'
    def getType(self):
        return "king"

    def getValue(self): 
        return self.value