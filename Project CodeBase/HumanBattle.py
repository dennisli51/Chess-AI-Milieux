import math, copy, random, time
from cmu_112_graphics import *
from pieces import *

#Splash Screen Mode and Player vs Player standard mode
class SplashScreenMode(Mode): 
    def appStarted(self):
        #background image taken from online url
        self.backgroundURL = 'https://wallpaperaccess.com/full/1307130.jpg'
        self.background = self.scaleImage(self.loadImage(self.backgroundURL), 0.65)

    def redrawAll(self, canvas):
        font = 'Arial 25 bold'
        canvas.create_image(650, 170, image=ImageTk.PhotoImage(self.background))

        canvas.create_rectangle(500, 50, 900, 150, fill = 'tan')
        canvas.create_rectangle(400, 200, 1000, 300, fill = 'green')
        canvas.create_rectangle(400, 300, 1000, 400, fill = 'yellow')
        canvas.create_rectangle(400, 400, 1000, 500, fill = 'red')
        canvas.create_text(self.width/2, 100, text='Chess AI Mileux', 
                            font='Arial 35 bold')
        canvas.create_text(self.width/2, 250, text=
                            'Press 1 for Player vs Player', font=font)
        canvas.create_text(self.width/2, 350, text='Press 2 for Player vs AI', 
                            font=font)
        canvas.create_text(self.width/2, 450, 
                        text='Press 3 for AI vs AI Demonstration', font=font)

    def keyPressed(mode, event):
        if event.key == "1": 
            mode.app.setActiveMode(mode.app.gameMode)
        if event.key == "2": 
            mode.app.setActiveMode(mode.app.manMachine)
        if event.key == "3": 
            mode.app.setActiveMode(mode.app.machineBattle)

class GameMode(Mode): #Standard 1v1 Chess
    whitePawn = Pawn('white')
    whiteKnight = Knight('white')
    whiteBishop = Bishop('white')
    whiteRook = Rook('white')
    whiteQueen = Queen('white')
    whiteKing = King('white')
    blackPawn = Pawn('black')
    blackKnight = Knight('black')
    blackBishop = Bishop('black')
    blackRook = Rook('black')
    blackQueen = Queen('black')
    blackKing = King('black')

    def appStarted(self):
        self.margin = 5
        self.gridHeight = self.gridWidth = self.height - 2*self.margin
        self.pressRow = None; self.pressCol = None
        self.setUpPieces()
        
    def timerFired(self):
        self.constantlyCheck() 
    
    def constantlyCheck(self): 
        #Helper function for timerfired for ease of other modes
        #Last 2 lines of code (marked with #) for first 2 if statements come from the following site:
        #https://www.geeksforgeeks.org/how-to-create-a-countdown-timer-using-python/
        if self.lastMove != ((None, None), (None, None)) and self.turn == 'black' and self.gameOver == False:
            self.blackTime -= 1
            mins, secs = divmod(self.blackTime, 60) #
            self.blackTimer = '{:02d}:{:02d}'.format(mins, secs) #
        if self.lastMove != ((None, None), (None, None)) and self.turn == 'white' and self.gameOver == False:
            self.whiteTime -= 1
            mins, secs = divmod(self.whiteTime, 60) #
            self.whiteTimer = '{:02d}:{:02d}'.format(mins, secs) #
        if self.whiteTime == 0:
            self.gameOver = True
            self.blackWins = True
            self.whiteTimer = 'Game Over, White Ran Out of Time'
            return
        elif self.blackTime == 0:
            self.gameOver = True
            self.whiteWins = True
            self.blackTimer = 'Game Over, White Ran Out of Time'
            return
        if self.checkCheck('white', self.boardPieces, self.whiteKingPos) == True: 
            self.whiteInCheck = True
        else: 
            self.whiteInCheck = False
        if self.checkCheck('black', self.boardPieces, self.blackKingPos) == True: 
            self.blackInCheck = True
        else: 
            self.blackInCheck = False
        #white in checkmate?
        if self.turn == 'white' and self.whiteInCheck == True:
            for row in range(8):
                for col in range(8):
                    if self.hasLegalMove('white', (row, col), self.boardPieces)[0] == True: 
                        self.gameOver = False
                        return
            self.gameOver = True
            self.blackWins = True
            self.whiteInCheck = False
        #black in checkmate?
        elif self.turn == 'black' and self.blackInCheck == True:
            for row in range(8):
                for col in range(8):
                    if self.hasLegalMove('black', (row, col), self.boardPieces)[0] == True: 
                        self.gameOver = False
                        return
            self.gameOver = True
            self.whiteWins = True
            self.blackInCheck = False
        #white in stalemate?
        elif self.turn == 'white' and self.checkCheck('white', self.boardPieces, self.whiteKingPos) == False:
            for row in range(8):
                for col in range(8):
                    if self.hasLegalMove('white', (row, col), self.boardPieces)[0] == True: 
                        self.gameOver = False
                        self.stalemate = False
                        return
            self.gameOver = True
            self.stalemate = True
        #black in stalemate?
        elif self.turn == 'black' and self.checkCheck('black', self.boardPieces, self.whiteKingPos) == False:
            for row in range(8):
                for col in range(8):
                    if self.hasLegalMove('black', (row, col), self.boardPieces)[0] == True: 
                        self.gameOver = False
                        self.stalemate = False
                        return
            self.gameOver = True
            self.stalemate = True
            
    def mousePressed(self, event):
        self.mousePressHelp(event)
            
    def mousePressHelp(self, event):
        if not self.pointInGrid(event.x, event.y): 
            return
        elif self.gameOver == True:
            return 
        #Mouse Pressed in Board Interactions
        #If no previous piece has already been selected:
        elif (self.pressRow, self.pressCol) == (None, None):
            self.pressRow, self.pressCol = self.getCell(event.x, event.y)
            if self.boardPieces[self.pressRow][self.pressCol] == None:
                #person tries to move a piece from an empty square
                self.pressRow, self.pressCol = (None, None)
            else: 
                #highlight piece clicked
                self.boardHighlight[self.pressRow][self.pressCol] = True

        elif (0 <= self.pressRow <= 7 and 0 <= self.pressCol <= 7
            and self.boardPieces[self.pressRow][self.pressCol] != None):
            #person has already selected a piece to move
            originalObj = self.boardPieces[self.pressRow][self.pressCol]
            originalImg = self.boardView[self.pressRow][self.pressCol]
            newRow, newCol = self.getCell(event.x, event.y)
            #Legality Check
            if not (self.isValidMove(originalObj, (self.pressRow, 
                    self.pressCol), self.getCell(event.x, event.y), self.boardPieces)): 
                self.pressRow, self.pressCol = (None, None)
                self.boardHighlight = self.make2dList(8,8)
                print('Illegal Move! Try a different one.')
                return 

            elif self.turn != originalObj.getColor(): #Wrong player's turn
                print('Wrong Turn!')
                return False

            #Test for safety of king if this move were to be made
            testBoard = copy.deepcopy(self.boardPieces)
            testBoard[self.pressRow][self.pressCol] = None
            testRow, testCol = self.getCell(event.x, event.y)
            testBoard[newRow][newCol] = originalObj
            if originalObj.getType() == 'king':
                if originalObj.getColor() == 'black':
                    kingPos = (testRow, testCol)
                elif originalObj.getColor() == 'white':
                    kingPos = (testRow, testCol)
            elif originalObj.getColor() == 'white':
                kingPos = self.whiteKingPos
            elif originalObj.getColor() == 'black':
                kingPos = self.blackKingPos
            if self.checkCheck(originalObj.getColor(), testBoard, kingPos) == True: 
                self.pressRow, self.pressCol = (None, None)
                self.boardHighlight = self.make2dList(8,8)
                print('King would be in check!')
                return
            
            #Consider if corner rooks have made a move yet
            if originalObj.getType() == 'rook' and originalObj.getColor() == 'white':
                if (self.pressRow, self.pressCol) == (7, 0): 
                    self.whiteQRookMoved = True
                elif (self.pressRow, self.pressCol) == (7, 7): 
                    self.whiteKRookMoved = True
            elif originalObj.getType() == 'rook' and originalObj.getColor() == 'black':
                if (self.pressRow, self.pressCol) == (0, 0): 
                    self.blackQRookMoved = True
                elif (self.pressRow, self.pressCol) == (0, 7): 
                    self.blackKRookMoved = True
            
            oldSq = (self.pressRow, self.pressCol)
            #Update King position
            if originalObj.getType() == 'king':
                if originalObj.getColor() == 'black':
                    self.blackKingPos = (newRow,  newCol)
                elif originalObj.getColor() == 'white':
                    self.whiteKingPos = (newRow, newCol)

            #Consider if first king move
            if originalObj.getType() =='king' and originalObj.getColor() =='white' and self.whiteKingMoved ==False:
                self.whiteKingMoved = True
                if newCol == 2 and self.whiteQRookMoved == False: 
                    self.boardPieces[7][3] = self.whiteRook
                    self.boardView[7][3] = self.loadImage(self.whiteRook.getImage())
                    self.boardPieces[7][0] = None
                    self.boardView[7][0] = None
                if newCol == 6 and self.whiteKRookMoved == False: 
                    self.boardPieces[7][5] = self.whiteRook
                    self.boardView[7][5] = self.loadImage(self.whiteRook.getImage())
                    self.boardPieces[7][7] = None
                    self.boardView[7][7] = None
            elif originalObj.getType() == 'king' and originalObj.getColor() == 'black' and self.blackKingMoved == False:
                self.blackKingMoved = True
                if newCol == 2 and self.whiteQRookMoved == False: 
                    self.boardPieces[0][3] = self.blackRook
                    self.boardView[0][3] = self.loadImage(self.blackRook.getImage())
                    self.boardPieces[0][0] = None
                    self.boardView[0][0] = None
                if newCol == 6 and self.whiteKRookMoved == False: 
                    self.boardPieces[0][5] = self.blackRook
                    self.boardView[0][5] = self.loadImage(self.blackRook.getImage())
                    self.boardPieces[0][7] = None
                    self.boardView[0][7] = None

            #Consider En passant
            if (originalObj.getType() == 'pawn' and originalObj.getColor() == 'white'
                and newRow == 2 and newCol != oldSq[1] and self.boardPieces[newRow][newCol] == None):
                self.boardPieces[self.pressRow][newCol] = None
                self.boardView[self.pressRow][newCol] = None
                
            elif (originalObj.getType() == 'pawn' and originalObj.getColor() == 'black'
                and newRow == 5 and newCol != oldSq[1] and self.boardPieces[newRow][newCol] == None):
                self.boardPieces[self.pressRow][newCol] = None
                self.boardView[self.pressRow][newCol] = None    

            #Modify the boardPieces 2d list and modify boardView 2d list
            self.boardPieces[self.pressRow][self.pressCol] = None
            self.boardView[self.pressRow][self.pressCol] = None
            self.pressRow, self.pressCol = self.getCell(event.x, event.y)
            self.boardPieces[self.pressRow][self.pressCol] = originalObj 
            self.boardView[self.pressRow][self.pressCol] = originalImg

            #Consider Promotion: 
            if (originalObj.getType() == 'pawn' and self.pressRow == 0 and 
                originalObj.getColor() == 'white'): 
                self.boardPieces[self.pressRow][self.pressCol] = self.whiteQueen
                self.boardView[self.pressRow][self.pressCol] = self.loadImage(self.whiteQueen.getImage())
            elif (originalObj.getType() == 'pawn' and self.pressRow == 7 and 
                originalObj.getColor() == 'black'):
                self.boardPieces[self.pressRow][self.pressCol] = self.blackQueen
                self.boardView[self.pressRow][self.pressCol] = self.loadImage(self.blackQueen.getImage())
            #Reset to new move and remove highlight
            if self.turn == 'white': self.turn = 'black'
            elif self.turn == 'black': self.turn = 'white'
            self.lastMove = ((oldSq[0], oldSq[1]), (self.pressRow, self.pressCol))
            self.moveHistory += [(originalObj.getType(), oldSq[0], oldSq[1], self.pressRow, self.pressCol)]
            self.pressRow, self.pressCol = (None, None)
            self.boardHighlight = self.make2dList(8,8)
            
    def keyPressed(self, event):
        if (event.key == 'b'):
            self.app.setActiveMode(self.app.splashScreenMode)
        if (event.key == 'r'):
            self.setUpPieces()

    def hasLegalMove(self, color, pieceSq, board): 
        #Takes in a piece, see if you can make a legal move with it
        #Checkmate checking algorithm 
        r,c = pieceSq[0], pieceSq[1]
        piece = board[r][c]
        if piece == None: return (False, (None, None))
        if piece.getColor() != color: return (False, (None, None))
        typeToCheck = None
        if color == 'white': 
            kingRow, kingCol = self.whiteKingPos
            typeToCheck = 'black'
        elif color == 'black':  
            kingRow, kingCol = self.blackKingPos
            typeToCheck = 'white'
        for row in range(8):
            for col in range(8):
                if (self.isValidMove(piece, (r,c), (row, col), board) == True):
                    #Test a move
                    testBoard = copy.deepcopy(board)
                    testBoard[r][c] = None
                    testBoard[row][col] = piece
                    if piece.getType() == 'king':
                        kingPos = (row, col)
                    else: kingPos = (kingRow, kingCol)
                    if not (self.checkCheck(color, testBoard, kingPos) == True):
                        return (True, (row, col))
        return (False, (None, None))

    def checkCheck(self, color, board, kingPos): #Check if the color's king is under attack
        kingRow, kingCol = (kingPos[0], kingPos[1])
        typeToCheck = None
        if color == 'white': 
            typeToCheck = 'black'
        elif color == 'black':  
            typeToCheck = 'white'

        for row in range(8):
            for col in range(8):
                if (board[row][col] != None and 
                    board[row][col].getColor() == typeToCheck):
                    piece = board[row][col]
                    if self.isValidMove(piece, (row, col), (kingRow, kingCol), board) == True:
                        return True
        return False

    def isValidMove(self, piece, start, end, board): 
        #Determines if a given piece move from 2 squares is legal (Doesn't consider checks)
        x1, y1 = start[0], start[1]
        x2, y2 = end[0], end[1]
        if (board[x2][y2] != None and piece.getColor() == 
            board[x2][y2].getColor()):
            return False #Can't take own piece

        elif (piece.getType() == 'king'): 
            #Castling check
            if piece.getColor() == 'white' and (x1, y1) == (7, 4) and (x2, y2) == (7, 6):
                if self.checkCheck('white', board, self.whiteKingPos): return False
                if self.whiteKingMoved == True: return False
                if self.whiteKRookMoved == True: return False
                if board[7][5] != None: return False
                if board[7][6] != None: return False
                else: return True
            elif piece.getColor() == 'white' and (x1, y1) == (7, 4) and (x2, y2) == (7, 2):
                if self.checkCheck('white', board, self.whiteKingPos): return False
                if self.whiteKingMoved == True: return False
                if self.whiteQRookMoved == True: return False
                if board[7][3] != None: return False
                if board[7][2] != None: return False
                if board[7][1] != None: return False
                else: return True
            elif piece.getColor() == 'black' and (x1, y1) == (0, 4) and (x2, y2) == (0, 6):
                if self.checkCheck('black', board, self.blackKingPos): return False
                if self.blackKingMoved == True: return False
                if self.blackKRookMoved == True: return False
                if board[0][5] != None: return False
                if board[0][6] != None: return False
                else: return True
            elif piece.getColor() == 'black' and (x1, y1) == (0, 4) and (x2, y2) == (0, 2):
                if self.checkCheck('black', board, self.blackKingPos): return False
                if self.blackKingMoved == True: return False
                if self.blackQRookMoved == True: return False
                if board[0][3] != None: return False
                if board[0][2] != None: return False
                if board[0][1] != None: return False
                else: return True
            #Move is in a 1 square radius
            kingMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), 
                        (1, 0), (1, 1)]
            dx, dy = ((x2-x1), (y2-y1))
            if (dx, dy) not in kingMoves: return False

        elif (piece.getType() == 'queen'):
            if (not(x1 == x2 or y1 == y2)) and (not(abs(x1-x2) == abs(y1 - y2))):
                return False
            else: 
                #Rook Move Type Check
                if y1  == y2: 
                    sq1 = min(x1, x2)
                    sq2 = max(x1, x2)
                    for sq in range(sq1+1, sq2): 
                        if board[sq][y1] != None: return False
                elif x1 == x2:
                    sq1 = min(y1, y2)
                    sq2 = max(y1, y2)
                    for sq in range(sq1+1, sq2): 
                        if board[x1][sq] != None: return False
                #Bishop Move Type Check
                elif x1 > x2 and y1 > y2: 
                    for sq in range(1, x1-x2):
                        if board[x1 - sq][y1 - sq] != None: 
                            return False
                elif x1 < x2 and y1 > y2: 
                    for sq in range(1, x2-x1):
                        if board[x1 + sq][y1 - sq] != None: 
                            return False
                elif x1 > x2 and y1 < y2:
                    for sq in range(1, x1 - x2):
                        if board[x1 - sq][y1 + sq] != None: 
                            return False
                elif x1 < x2 and y1 < y2: 
                    for sq in range(1, x2-x1):
                        if board[x1 + sq][y1 + sq] != None: 
                            return False        

        elif (piece.getType() == 'rook'):
            if not(x1 == x2 or y1 == y2): 
                return False
            else: 
                if y1  == y2: 
                    sq1 = min(x1, x2)
                    sq2 = max(x1, x2)
                    for sq in range(sq1+1, sq2): 
                        if board[sq][y1] != None: return False
                elif x1 == x2:
                    sq1 = min(y1, y2)
                    sq2 = max(y1, y2)
                    for sq in range(sq1+1, sq2): 
                        if board[x1][sq] != None: return False

        elif (piece.getType() == 'bishop'):
            if not(abs(x1-x2) == abs(y1 - y2)):
                return False
            else: 
                if x1 > x2 and y1 > y2: 
                    for sq in range(1, x1-x2):
                        if board[x1 - sq][y1 - sq] != None: 
                            return False
                elif x1 < x2 and y1 > y2: 
                    for sq in range(1, x2-x1):
                        if board[x1 + sq][y1 - sq] != None: 
                            return False
                elif x1 > x2 and y1 < y2:
                    for sq in range(1, x1 - x2):
                        if board[x1 - sq][y1 + sq] != None: 
                            return False
                elif x1 < x2 and y1 < y2: 
                    for sq in range(1, x2-x1):
                        if board[x1 + sq][y1 + sq] != None: 
                            return False

        elif (piece.getType() == 'knight'):
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            if dx == 1 and dy == 2: pass
            elif dx == 2 and dy == 1: pass
            else: return False

        elif (piece.getType() == 'pawn'):
            if piece.getColor() == 'white':
                if x2 >= x1: return False
                elif board[x2][y2] != None: 
                    dx, dy = ((x2-x1), (y2-y1))
                    whitePawnTake = [(-1, -1), (-1, 1)]
                    if (dx, dy) not in whitePawnTake: return False
                #En Passant
                elif (x1 == 3 and x2 == 2 and y1 > 0 and y2 == y1 - 1 and 
                      self.lastMove == ((x1-2, y2),(x1, y2)) and board[x1][y2].getType() == 'pawn'): 
                    pass
                elif (x1 == 3 and x2 == 2 and y1 < 7 and y2 == y1 + 1 and 
                      self.lastMove == ((x1-2, y2),(x1, y2)) and board[x1][y2].getType() == 'pawn'): 
                    pass
                elif y1 != y2: return False
                elif x1 == 6 and not (x2 == 5 or x2 == 4): 
                    return False
                elif x1 == 6 and x2 == 4 and board[5][y1] != None: 
                    return False
                elif x1 != 6 and x1 - x2 != 1: 
                    return False
                
            elif piece.getColor() == 'black': 
                if x1 >= x2: return False
                elif board[x2][y2] != None: 
                    dx, dy = ((x2-x1), (y2-y1))
                    whitePawnTake = [(1, 1), (1, -1)]
                    if (dx, dy) not in whitePawnTake: return False
                #En Passant
                elif (x1 == 4 and x2 == 5 and y1 > 0 and y2 == y1 - 1 and 
                      self.lastMove == ((x1+2, y2),(x1, y2)) and board[x1][y2].getType() == 'pawn'): 
                    pass
                elif (x1 == 4 and x2 == 5 and y1 < 7 and y2 == y1 + 1 and 
                      self.lastMove == ((x1+2, y2),(x1, y2)) and board[x1][y2].getType() == 'pawn'): 
                    pass
                elif y1 != y2: return False
                elif x1 == 1 and not (x2 == 2 or x2 == 3): 
                    return False
                elif x1 == 1 and x2 == 3 and board[2][y1] != None: 
                    return False
                elif x1 != 1 and x2 - x1 != 1: 
                    return False
        
        return True #Passed every condition

    def isAttacking(self, start, end): #check if piece at start pos can take end pos
        piece = self.boardPieces[start[0]][start[1]]
        if isLegalMove(self, piece, start, end): 
            return True
        else: 
            return False

    def pointInGrid(self, x, y): #Taken from 112 Animation Notes
        #https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        return ((self.margin <= x <= self.gridWidth-self.margin) and
                (self.margin <= y <= self.gridHeight-self.margin))

    def setUpPieces(self): 
        self.boardView = self.make2dList(8,8)
        self.boardPieces = self.make2dList(8,8)
        self.boardHighlight = self.make2dList(8,8)
        self.whiteKingMoved = False; self.blackKingMoved = False
        self.whiteQRookMoved = False; self.whiteKRookMoved = False
        self.blackQRookMoved = False; self.blackKRookMoved = False
        self.whiteKingPos = (7, 4); self.blackKingPos = (0, 4)
        
        #set up default starting position of a chess game
        self.boardPieces[0][0] = self.boardPieces[0][7] = self.blackRook
        self.boardPieces[7][7] = self.boardPieces[7][0] = self.whiteRook
        self.boardPieces[0][2] = self.boardPieces[0][5] = self.blackBishop
        self.boardPieces[7][2] = self.boardPieces[7][5] = self.whiteBishop
        self.boardPieces[0][1] = self.boardPieces[0][6] = self.blackKnight
        self.boardPieces[7][1] = self.boardPieces[7][6] = self.whiteKnight
        #set up Pawns
        for i in range (8):
            self.boardPieces[6][i] = self.whitePawn
            self.boardPieces[1][i] = self.blackPawn
        
        self.boardPieces[0][3] = self.blackQueen
        self.boardPieces[0][4] = self.blackKing 
        self.boardPieces[7][3] = self.whiteQueen
        self.boardPieces[7][4] = self.whiteKing  
        self.boardPieceCopy = copy.deepcopy(self.boardPieces) 
        self.turn = 'white'
        self.gameOver = self.stalemate = False
        self.whiteInCheck = self.blackInCheck = False 
        self.lastMove = ((None, None), (None, None))
        self.moveHistory = []
        self.whiteTime = self.blackTime = 300
        self.whiteTimer = self.blackTimer = '05:00'
        for row in range(8): 
            for col in range(8): 
                if self.boardPieces[row][col] != None:
                    location = self.boardPieces[row][col].getImage()
                    self.boardView[row][col] = self.loadImage(location)
        #Default player profile image taken from online URL
        self.playerURL = 'https://www.computerhope.com/jargon/g/guest-user.jpg'
        self.playerImage = self.scaleImage(self.loadImage(self.playerURL), 2/3)

    def make2dList(self, rows, cols): #taken from 112 Lists Notes
        #https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
        return [ ([None] * cols) for row in range(rows) ]

    def getCell(self, x, y): #Taken from 112 Animation Notes 
        #https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        if (not self.pointInGrid(x, y)):
            return (-1, -1)
        cellWidth  = self.gridWidth / 8
        cellHeight = self.gridHeight / 8
        row = int((y - self.margin) / cellHeight)
        col = int((x - self.margin) / cellWidth)

        return (row, col)

    def getCellBounds(self, row, col): #Taken from 112 Animation Notes then modified
        #https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        gridHeight = self.gridHeight
        gridWidth = gridHeight
        x0 = self.margin + gridWidth * col / 8
        x1 = self.margin + gridWidth * (col+1) / 8
        y0 = self.margin + gridHeight * row / 8
        y1 = self.margin + gridHeight * (row+1) / 8
        return (x0, y0, x1, y1)

    def drawCell(self, canvas, row, col, color): 
        #(Own function, not from 112 animation)
        (x1, y1, x2, y2) = self.getCellBounds(row, col)
        canvas.create_rectangle(x1, y1, x2, y2, fill = color)

    def drawPiece(self, canvas, row, col):
        (x1, y1, x2, y2) = self.getCellBounds(row, col)
        if self.boardView[row][col] == None: 
            return 
        canvas.create_image((x1+x2)/2, (y1+y2)/2, 
                        image=ImageTk.PhotoImage(self.boardView[row][col]))

    def drawPieces(self,canvas):
        for row in range(8):
            for col in range(8):
                self.drawPiece(canvas, row, col)

    def drawBoard(self, canvas): #draws Board
        color = ''
        for row in range(8): 
            for col in range(8): 
                if (row + col) % 2 == 0: 
                    color = 'blanchedalmond'
                else: 
                    color = 'darkgoldenrod'
                if self.boardHighlight[row][col] == True: 
                    color = 'lightblue'
                self.drawCell(canvas,row,col,color)

    def drawCheck(self, canvas): #Draws some text/visuals that should appear
        #across all 3 different types of gamemodes
        if self.whiteInCheck == True: 
            canvas.create_text(1220, 550, text = 'White King In Check'
                               , font = 'Arial 15 bold')
        elif self.blackInCheck== True: 
            canvas.create_text(1220, 550, text = 'Black King In Check'
                               , font = 'Arial 15 bold')
        if self.stalemate == True: 
            canvas.create_text(1220, 550, text = 'Whoops! Stalemate! Game Over.')
        elif self.gameOver == True: 
            if self.whiteWins == True:
                canvas.create_text(1050, 450, text = 'Game Over! White wins.'
                                   , font = 'Arial 15 bold')
            elif self.blackWins == True:
                canvas.create_text(1050, 450, text = 'Game Over! Black wins.'
                                   , font = 'Arial 15 bold')
        if self.turn == 'white':
            canvas.create_rectangle(700, 200, 1400, 300, fill = 'firebrick') 
            canvas.create_rectangle(700, 300, 1400, 400, fill = 'silver')
        elif self.turn == 'black':
            canvas.create_rectangle(700, 200, 1400, 300, fill = 'silver') 
            canvas.create_rectangle(700, 300, 1400, 400, fill = 'firebrick') 
        canvas.create_text(1050, 250, text = f'White\'s Time Remaining: {self.whiteTimer}', 
                            font = 'Arial 30 bold')
        canvas.create_text(1050, 350, text = f'Black\'s Time Remaining: {self.blackTimer}', 
                            font = 'Arial 30 bold') 
        canvas.create_rectangle(700, 600, 1400, 700)
        if len(self.moveHistory) > 0:
            last = self.moveHistory[-1]
            piece = last[0]
            startR, startC, endR, endC = last[1], last[2], last[3], last[4]
            canvas.create_text(920, 550, text = f'Last Move was {piece} from {startR,startC} to {endR, endC}.'
                               , font = 'Arial 16')
            
    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,self.width,self.height, fill = 'lightgray') 
        canvas.create_rectangle(700, 500, 1400, 700, fill = 'honeydew')
        canvas.create_rectangle(700, 200, 1400, 500, fill = 'honeydew')
        self.drawBoard(canvas)
        self.drawPieces(canvas)
        self.drawCheck(canvas)
        if self.gameOver == False:
            if self.turn == 'white': 
                canvas.create_text(1050, 450, text = 'White\'s Turn to make a move! Better Hurry Up!'
                                , font = 'Arial 20 bold')
            elif self.turn == 'black': 
                canvas.create_text(1050, 450, text = 'Black\'s Turn to make a move! Better Hurry Up'
                                , font = 'Arial 20 bold')
            
        canvas.create_image(800, 100, image=ImageTk.PhotoImage(self.playerImage))
        canvas.create_image(1300, 100, image=ImageTk.PhotoImage(self.playerImage))
        canvas.create_rectangle(900, 0, 1200, 200, fill = 'honeydew')
        canvas.create_text(1050, 50, text = 'PLAYER', font = 'Arial 20 bold')
        canvas.create_text(1050, 100, text = 'VS', font = 'Arial 20 bold')
        canvas.create_text(1050, 150, text = 'PLAYER', font = 'Arial 20 bold')
        
        canvas.create_text(850, 630, text = 'Key Commands Are:', font = 'Arial 18')
        canvas.create_text(1075, 630, text = '\'B\' to Return to Menu', font = 'Arial 15')
        canvas.create_text(1070, 665, text = '\'R\' to Restart Game', font = 'Arial 15')

