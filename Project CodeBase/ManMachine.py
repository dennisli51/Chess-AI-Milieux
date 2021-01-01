import math, copy, random, time
from cmu_112_graphics import *
from pieces import *
from HumanBattle import *

class ManMachine(GameMode): #Player vs AI Mode
    #Inherits all functions from gamemode class
    #Piece square tables and piece values of 8x8 advanced evaluation modified 
    #from https://www.chessprogramming.org/Simplified_Evaluation_Function
    #Reference for how I learned the intuition behind Minimax
    # and alpha beta pruning: https://www.youtube.com/watch?v=l-hh51ncgDI 
    
    def pieceSquareTables(self):
        self.whitePawnTable = [[0,  0,  0,  0,  0,  0,  0,  0],
                               [50, 50, 50, 50, 50, 50, 50, 50],
                               [10, 10, 20, 30, 30, 20, 10, 10],
                               [5,  5, 10, 25, 25, 10,  5,  5],
                               [0,  0,  0, 20, 20,  0,  0,  0],
                               [5, -5,-10,  0,  0,-10, -5,  5],
                               [5, 5, 5,-20,-20,  5 , 5 ,  5],
                               [0,  0,  0,  0,  0,  0,  0,  0]]
        self.blackPawnTable = [[0,  0,  0,  0,  0,  0,  0,  0],
                               [5, 5, 5,-20,-20, 5, 5,  5],
                               [5, -5, -10, 0,  0,-10, -5,  5],
                               [0,  0,  0, 20, 20,  0,  0,  0],
                               [5,  5, 10, 25, 25, 10,  5,  5],
                               [10, 10, 20, 30, 30, 20, 10, 10],
                               [50, 50, 50, 50, 50, 50, 50, 50],
                               [0,  0,  0,  0,  0,  0,  0,  0]]
        self.whiteKnightTable = [[-50,-40,-30,-30,-30,-30,-40,-50],
                                [-40,-20,  0,  0,  0,  0,-20,-40],
                                [-40,  0, 10, 15, 15, 10,  0,-40],
                                [-40,  5, 15, 20, 20, 15,  5,-40],
                                [-40,  0, 15, 20, 20, 15,  0,-40],
                                [-40,  5,  5, 15, 15,  5,  5,-40],
                                [-40,-20,  0,  5,  5,  0,-20,-40],
                                [-50,-40,-30,-30,-30,-30,-40,-50]]
        self.blackKnightTable = [[-50,-40,-30,-30,-30,-30,-40,-50], 
                                [-40,-20,  0,  5,  5,  0,-20,-40],
                                [-40,  5,  5, 15, 15,  5,  5,-40],
                                [-40,  0, 15, 20, 20, 15,  0,-40],
                                [-40,  5, 15, 20, 20, 15,  5,-40],
                                [-40,  0, 10, 15, 15, 10,  0,-40],
                                [-40,-20,  0,  0,  0,  0,-20,-40],
                                [-50,-40,-30,-30,-30,-30,-40,-50]]
        self.whiteBishopTable = [[-20,-10,-10,-10,-10,-10,-10,-20],
                                [-10,  0,  0,  0,  0,  0,  0,-10],
                                [-10,  0,  5,  5,  5,  5,  0,-10],
                                [-10,  5,  5,  5,  5,  5,  5,-10],
                                [-10,  0,  6, 5,  5,   6,  0,-10],
                                [-10, 10, 10, 5, 5, 10, 10,-10],
                                [-10,  5,  0,  0,  0,  0,  5,-10],
                                [-20,-10,-10,-10,-10,-10,-10,-20]]
        self.blackBishopTable = [[-20,-10,-10,-10,-10,-10,-10,-20], 
                                [-10,  5,  0,  0,  0,  0,  5,-10],
                                [-10, 10, 10, 5, 5, 10, 10,-10],
                                [-10,  0, 6 , 5, 5, 6,  0,-10],
                                [-10,  5,  5, 10, 10,  5,  5,-10],
                                [-10,  0,  5, 10, 10,  5,  0,-10],
                                [-10,  0,  0,  0,  0,  0,  0,-10],
                                [-20,-10,-10,-10,-10,-10,-10,-20]]
        self.whiteRookTable =   [[-5,  0,  0,  0,  0,  0,  0,  -5],
                                [ 5, 10, 10, 10, 10, 10, 10,  5],
                                [0,  0,  0,  0,  0,  0,  0, 0],
                                [0,  0,  0,  0,  0,  0,  0, 0],
                                [0,  0,  0,  0,  0,  0,  0, 0],
                                [0,  0,  0,  0,  0,  0,  0, 0],
                                [-5,  -5,  0,  0,  0,  0,  -5, -5],
                                [-5,  0,  0,  5,  5,  0,  0,  -5]]  
        self.blackRookTable =   [[ -5,  0,  0,  5,  5,  0,  0,  -5], 
                                [-5,  -5,  0,  0,  0,  0,  -5, -5],
                                [0,  0,  0,  0,  0,  0,  0, 0],
                                [0,  0,  0,  0,  0,  0,  0, 0],
                                [0,  0,  0,  0,  0,  0,  0, 0],
                                [0,  0,  0,  0,  0,  0,  0, 0],
                                [ 5, 10, 10, 10, 10, 10, 10,  5],
                                [-5,  0,  0,  0,  0,  0,  0,  -5]]  
        self.whiteQueenTable =  [[-20,-10,-10, -5, -5,-10,-10,-20],
                                [-10,  0,  0,  0,  0,  0,  0,-10],
                                [-10,  0,  4,  4,  4,  4,  0,-10],
                                [ -5,  0,  4,  4,  4,  4,  0, -5],
                                [  0,  0,  4,  4,  4,  4,  0, -5],
                                [-10,  5,  5,  4,  4,  5,  1,-10],
                                [-10,  0,  5,  5,  4,  0,  0,-10],
                                [-20,-10,-10, -5, -5,-10,-10,-20]]
        self.blackQueenTable =  [[-20,-10,-10, -5, -5,-10,-10,-20], 
                                [-10,  0,  5,  5,  4,  0,  0,-10],
                                [-10,  5,  5,  4,  4,  5,  0,-10],
                                [  0,  0,  4,  4,  4,  4,  0, -5],
                                [ -5,  0,  4,  4,  4,  4,  0, -5],
                                [-10,  0,  4,  4,  4,  4,  0,-10],
                                [-10,  0,  0,  0,  0,  0,  0,-10],
                                [-20,-10,-10, -5, -5,-10,-10,-20]]
        self.whiteKingTable =   [[-30,-40,-40,-50,-50,-40,-40,-30],
                                [-30,-40,-40,-50,-50,-40,-40,-30],
                                [-30,-40,-40,-50,-50,-40,-40,-30],
                                [-30,-40,-40,-50,-50,-40,-40,-30],
                                [-20,-30,-30,-40,-40,-30,-30,-20],
                                [-10,-20,-20,-20,-20,-20,-20,-10],
                                [ 20, 20,  0,  0,  0,  0, 20, 20],
                                [ 20, 30, 10,  0,  0, 10, 30, 20]]
        self.blackKingTable =   [[ 20, 30, 10,  0,  0, 10, 30, 20], 
                                [ 20, 20,  0,  0,  0,  0, 20, 20],
                                [-10,-20,-20,-20,-20,-20,-20,-10],
                                [-20,-30,-30,-40,-40,-30,-30,-20],
                                [-30,-40,-40,-50,-50,-40,-40,-30],
                                [-30,-40,-40,-50,-50,-40,-40,-30],
                                [-30,-40,-40,-50,-50,-40,-40,-30],
                                [-30,-40,-40,-50,-50,-40,-40,-30]]
        
    def appStarted(self):
        self.margin = 5
        self.gridHeight = self.gridWidth = self.height - 2*self.margin
        self.pressRow = None; self.pressCol = None
        self.setUpPieces()
        self.machineLevel = None
        self.pieceSquareTables()
        self.pieceEval = self.materialEval = 0
        #Image taken from online
        self.aiURL = 'https://i.pinimg.com/originals/f0/2d/81/f02d81ee7d2ccd7c89ecf792f23e02c2.jpg'
        self.aiImage = self.scaleImage(self.loadImage(self.aiURL), 0.3)

    def timerFired(self):
        self.constantlyCheck() 
        #Unique Aspects of manMachine Subclass:
        if self.turn == 'black' and self.gameOver == False and self.machineLevel != None:
            self.botMove(self.machineLevel, 'black', self.boardPieces, self.boardView)
        self.materialEval = self.boardEval(self.boardPieces, 'white')
        self.pieceEval = self.squareTableEval(self.boardPieces, 'white')
            
    def botMove(self, depth, color, boardPieces, boardView): 
        #Helper for letting the bot actually move
        bestMove = self.machineCalc(depth, color)
        start, end = bestMove[0], bestMove[1]
        startRow = start[0]; startCol = start[1]
        endRow = end[0]; endCol = end[1]
        originalObj = boardPieces[startRow][startCol]
        originalImg = boardView[startRow][startCol]
        if originalObj == None: 
            return
        #Consider if first king move, and update if a castling move was made
        if originalObj.getType() =='king' and originalObj.getColor() =='white' and self.whiteKingMoved ==False:
            self.whiteKingMoved = True
            if endRow == 7 and endCol == 2 and self.whiteQRookMoved == False: 
                boardPieces[7][3] = self.whiteRook
                boardView[7][3] = self.loadImage(self.whiteRook.getImage())
                boardPieces[7][0] = None
                boardView[7][0] = None
            if endRow == 7 and endCol == 6 and self.whiteKRookMoved == False: 
                boardPieces[7][5] = self.whiteRook
                boardView[7][5] = self.loadImage(self.whiteRook.getImage())
                boardPieces[7][7] = None
                boardView[7][7] = None
        elif originalObj.getType() == 'king' and originalObj.getColor() == 'black' and self.blackKingMoved == False:
            self.blackKingMoved = True
            if endRow == 0 and endCol == 2 and self.blackQRookMoved == False: 
                boardPieces[0][3] = self.blackRook
                boardView[0][3] = self.loadImage(self.blackRook.getImage())
                boardPieces[0][0] = None
                self.boardView[0][0] = None
            if endRow == 0 and endCol == 6 and self.blackKRookMoved == False: 
                boardPieces[0][5] = self.blackRook
                boardView[0][5] = self.loadImage(self.blackRook.getImage())
                boardPieces[0][7] = None
                boardView[0][7] = None        
        if originalObj.getType() == 'king' and originalObj.getColor() == color:
            if color == 'black':
                self.blackKingPos = (endRow,  endCol) #Change King Pos
                self.blackKingMoved = True
            elif color == 'white': 
                self.whiteKingPos = (endRow,  endCol) #Change King Pos
                self.whiteKingMoved = True        
        if originalObj.getType() == 'rook' and originalObj.getColor() == color:
            #Update the fact that a corner rook has moved so castling there isn't possible
            if (startRow, startCol) == (0, 0): 
                self.blackQRookMoved = True
            elif (startRow, startCol) == (0, 7): 
                self.blackKRookMoved = True  
            elif (startRow, startCol) == (7, 0): 
                self.whiteQRookMoved = True
            elif (startRow, startCol) == (7, 7): 
                self.whiteKRookMoved = True      
        #En passant
        if (originalObj.getType() == 'pawn' and originalObj.getColor() == 'black'
                and endRow == 5 and endCol != startCol and self.boardPieces[endRow][endCol] == None):
                boardPieces[startRow][endCol] = None
                boardView[startRow][endCol] = None  
        elif (originalObj.getType() == 'pawn' and originalObj.getColor() == 'white'
                and endRow == 2 and endCol != startCol and self.boardPieces[endRow][endCol] == None):
                boardPieces[startRow][endCol] = None
                boardView[startRow][endCol] = None  
        #Modify board
        boardPieces[startRow][startCol] = None
        boardView[startRow][startCol] = None
        boardPieces[endRow][endCol] = originalObj 
        boardView[endRow][endCol] = originalImg
        self.lastMove = ((startRow, startCol), (endRow, endCol))
        self.moveHistory += [(originalObj.getType(), startRow, startCol, endRow, endCol)]

        if color == 'black': self.turn = 'white'
        elif color == 'white': self.turn = 'black'

        #Consider Promotion: 
        if (originalObj.getType() == 'pawn' and color == 'black' and startRow == 6):
            self.boardPieces[endRow][endCol] = self.blackQueen
            self.boardView[endRow][endCol] = self.loadImage(self.blackQueen.getImage())
        elif (originalObj.getType() == 'pawn' and color == 'white' and startRow == 1):
            self.boardPieces[endRow][endCol] = self.whiteQueen
            self.boardView[endRow][endCol] = self.loadImage(self.whiteQueen.getImage())

    def machineCalc(self, depth, color): #return best move to play based on depth to use
        startRow = startCol = endRow = endCol = None
        previous = prevStartRow = prevStartCol = prevEndRow = prevEndCol = None
        if len(self.moveHistory) > 4:
            previous = self.moveHistory[-4]
            prevStartRow, prevStartCol = (previous[1], previous[2])
            prevEndRow, prevEndCol = (previous[3], previous[4])
            previous = previous[0]
            
        #Depth 0: Random-ish Moves (the computer plays the first pseudo-random legal move it sees)
        if depth == 0:
            while True: 
                row = random.randint(0, 7)
                col = random.randint(0, 7)
                if (self.boardPieces[row][col] != None and self.boardPieces[row][col].getColor() == color):
                    if self.hasLegalMove(color, (row, col), self.boardPieces)[0] == True:
                        end = self.hasLegalMove(color, (row, col), self.boardPieces)[1]
                        startRow, startCol = (row, col)
                        endRow, endCol = (end[0], end[1])
                        return ((startRow, startCol), (endRow, endCol))
        #Depth 1: Captures any piece it sees, ignore piece placement or consequence
        if depth == 1: 
            maxPts = self.boardEval(self.boardPieces, color)
            for row in range (8):
                for col in range(7, -1, -1):
                    #Find every piece on the board
                    if (self.boardPieces[row][col] != None and self.boardPieces[row][col].getColor() == color
                        and self.hasLegalMove(color, (row, col), self.boardPieces)[0] == True):
                        piece = self.boardPieces[row][col]
                        #find everywhere this piece can move and compare how much material it gains
                        for endR in range (8):
                            for endC in range (8):
                                if self.isValidMove(piece, (row, col), (endR, endC), self.boardPieces):
                                    testBoard = copy.deepcopy(self.boardPieces)
                                    testBoard[row][col] = None
                                    testBoard[endR][endC] = piece
                                    if piece.getType() == 'king':
                                        kingPos = (endR, endC)
                                    else: kingPos = (self.blackKingPos)
                                    #ensure legality of move, both of check and by isValidMove()
                                    if self.checkCheck(color, testBoard, kingPos) == True:
                                        pass
                                    elif (piece == previous and row == prevStartRow and 
                                          col == prevStartCol and endR == prevEndRow 
                                          and endC == prevEndCol):
                                        pass #try to avoid repetition of move
                                    elif (30 < len(self.moveHistory) < 50 and (piece, row, col,
                                        endR, endC) in self.moveHistory):
                                        print('woops')
                                        pass #avoid repeating moves in the middlegame
                                    elif color == 'black':
                                        if (self.boardEval(testBoard, color) <= maxPts and 
                                        self.checkCheck(color, testBoard, kingPos) == False):
                                            maxPts = self.boardEval(testBoard, color)                            
                                            startRow, startCol = (row, col)
                                            endRow, endCol = (endR, endC) 
                                    elif color == 'white': 
                                        if (self.boardEval(testBoard, color) >= maxPts and 
                                        self.checkCheck(color, testBoard, kingPos) == False):
                                            maxPts = self.boardEval(testBoard, color)                            
                                            startRow, startCol = (row, col)
                                            endRow, endCol = (endR, endC) 
            if maxPts == self.boardEval(self.boardPieces, color): 
                #randomize move if no option maximizes material gain in 1 turn
                while True: 
                    row = random.randint(0, 7)
                    col = random.randint(0, 7)
                    if (self.boardPieces[row][col] != None and self.boardPieces[row][col].getColor() == color):
                        if self.hasLegalMove(color, (row, col), self.boardPieces)[0] == True:
                            end = self.hasLegalMove(color, (row, col), self.boardPieces)[1]
                            startRow, startCol = (row, col)
                            endRow, endCol = (end[0], end[1])
                            return ((startRow, startCol), (endRow, endCol))
            return ((startRow, startCol), (endRow, endCol))        
        #Depth 2 or more: Consider piece placement and material, search using Minimax helper
        elif depth >= 2: 
            compareEval, startRow, startCol, endRow, endCol = self.miniMaxHelp(self.boardPieces, depth, color, -99999, 99999)     
            return ((startRow, startCol), (endRow, endCol))
                
    def miniMaxHelp(self, board, depth, side, whiteScore, blackScore): 
        #Minimax Algorithm with Alpha Beta Pruning
        if side == 'black': tryToMax = False #Let true/false represent maximizing or minimizing
        elif side == 'white': tryToMax = True 
        else: tryToMax = side
        startRow = startCol = endRow = endCol = 0
        if depth == 0: #Base Case: Reached end of recursive search tree
            placementEval = self.squareTableEval(board, 'white')
            materialEval = self.boardEval(board, 'white')
            return (materialEval + placementEval, None, None, None, None)
        #Recursively search deeper into the tree if it is not yet at final depth
        if tryToMax == True: 
            compareMax = -999999 #set very negative lower value to try to maximize
            for row in range (8):
                for col in range(8):
                    #find all your pieces
                    if (self.boardPieces[row][col] != None and self.boardPieces[row][col].getColor() == 'white'
                        and self.hasLegalMove('white', (row, col), self.boardPieces)[0] == True):
                        piece = self.boardPieces[row][col]
                        for endR in range (8):
                            for endC in range (8):
                                #figure out where each of your pieces can move
                                if self.isValidMove(piece, (row, col), (endR, endC), self.boardPieces):
                                    testBoard = copy.deepcopy(board)
                                    testBoard[row][col] = None
                                    testBoard[endR][endC] = piece
                                    if piece.getType() == 'king':
                                        kingPos = (endR, endC)
                                    else: kingPos = (self.whiteKingPos)
                                    #ensure legality of move, both of check and by isValidMove()
                                    if self.checkCheck('white', testBoard, kingPos) == True:
                                        pass
                                    else: #see if this is a better maximizing opportunity
                                        compareEval = self.miniMaxHelp(testBoard, depth - 1, 
                                                                       (not tryToMax), whiteScore, blackScore)[0]
                                        if compareEval >= compareMax: 
                                            compareMax = compareEval 
                                            startRow, startCol = (row, col)
                                            endRow, endCol = (endR, endC)
                                        whiteScore = max(whiteScore, compareEval)
                                        if whiteScore > blackScore: 
                                            return (compareMax, startRow, startCol, endRow, endCol)
            return (compareMax, startRow, startCol, endRow, endCol)
        elif tryToMax == False: 
            compareMin = 999999 #set very high value to try to minimize
            for row in range (8):
                for col in range(8):
                    if (self.boardPieces[row][col] != None and self.boardPieces[row][col].getColor() == 'black'
                        and self.hasLegalMove('black', (row, col), self.boardPieces)[0] == True):
                        piece = self.boardPieces[row][col]
                        for endR in range (8):
                            for endC in range (8):
                                if self.isValidMove(piece, (row, col), (endR, endC), self.boardPieces):
                                    testBoard = copy.deepcopy(board)
                                    testBoard[row][col] = None
                                    testBoard[endR][endC] = piece
                                    if piece.getType() == 'king':
                                        kingPos = (endR, endC)
                                    else: kingPos = (self.blackKingPos)
                                    #ensure legality of move, both of check and by isValidMove()
                                    if self.checkCheck('black', testBoard, kingPos) == True:
                                        pass
                                    else: 
                                        compareEval = self.miniMaxHelp(testBoard, depth - 1, 
                                                                       (not tryToMax), whiteScore, blackScore)[0]
                                        if compareEval < compareMin: 
                                            compareMin = compareEval 
                                            startRow, startCol = (row, col)
                                            endRow, endCol = (endR, endC)
                                        blackScore = min(compareEval, blackScore)
                                        if whiteScore > blackScore: 
                                            return (compareMin, startRow, startCol, endRow, endCol)
            return (compareMin, startRow, startCol, endRow, endCol)          
        
    def boardEval(self, board, side): #takes in a board and returns value of pieces
        #Naive evaluation that counts only the point values of the pieces, not the squares they are on
        factor = evaluation = 0
        if side == True: 
            factor = 1
            side = 'white'
        elif side == False: 
            factor = -1
            side == 'black'
        for row in range(8):
            for col in range(8):
                if board[row][col] != None: 
                    if board[row][col].getColor() == 'white':
                        evaluation += board[row][col].getValue()
                    elif board[row][col].getColor() == 'black':
                        evaluation -= board[row][col].getValue()
        for row in range(8):
            for col in range(8):
                if self.hasLegalMove(side, (row, col), self.boardPieces)[0] == True: 
                    return evaluation
                elif (board[row][col]!= None and board[row][col].getType() == 'king' and
                      board[row][col].getColor() == side):
                    kingPos = (row, col)
        if self.checkCheck(side, board, kingPos): 
            return factor*99999 #Checkmate has occured
        else: return 0 #stalemate has occured
                        
    def squareTableEval(self, board, maxSide): #Evaluate positions not just based on the 
        #material count but also consider where the pieces are located. Enables AI
        #to begin thinking beyond material and about strategic strengths of piece placement
        whiteSum = 0
        blackSum = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] != None: 
                    if board[row][col].getColor() == 'white':
                        if board[row][col].getType() == 'pawn':
                            whiteSum += self.whitePawnTable[row][col]
                        elif board[row][col].getType() == 'knight':
                            whiteSum += self.whiteKnightTable[row][col]
                        elif board[row][col].getType() == 'bishop':
                            whiteSum += self.whiteBishopTable[row][col]
                        elif board[row][col].getType() == 'rook':
                            whiteSum += self.whiteRookTable[row][col]
                        elif board[row][col].getType() == 'queen':
                            whiteSum += self.whiteQueenTable[row][col]
                        elif board[row][col].getType() == 'king':
                            whiteSum += self.whiteKingTable[row][col]
                    elif board[row][col].getColor() == 'black':
                        if board[row][col].getType() == 'pawn':
                            blackSum += self.blackPawnTable[row][col]
                        elif board[row][col].getType() == 'knight':
                            blackSum += self.blackKnightTable[row][col]
                        elif board[row][col].getType() == 'bishop':
                            blackSum += self.blackBishopTable[row][col]
                        elif board[row][col].getType() == 'rook':
                            blackSum += self.blackRookTable[row][col]
                        elif board[row][col].getType() == 'queen':
                            blackSum += self.blackQueenTable[row][col]
                        elif board[row][col].getType() == 'king':
                            blackSum += self.blackKingTable[row][col]
        return whiteSum - blackSum

    def mousePressed(self, event):
        if self.pointInGrid(event.x, event.y) and self.turn == 'black':
            return 
        elif self.machineLevel == None and self.pointInGrid(event.x, event.y):
            return
        #call all original functions of gameMode's superclass mousePressed
        self.mousePressHelp(event)
        
    def keyPressed(self, event):
        if (event.key == 'b'):
            self.app.setActiveMode(self.app.splashScreenMode)
        if (event.key == 'r'):
            self.setUpPieces()
            self.machineLevel = None
        if event.key.isdigit() and self.machineLevel == None and 0 <= int(event.key) < 4:
            self.machineLevel = int(event.key)
        
    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,self.width,self.height, fill = 'lightgray') 
        canvas.create_rectangle(700, 500, 1400, 700, fill = 'honeydew')
        canvas.create_rectangle(700, 200, 1400, 500, fill = 'honeydew')
        self.drawBoard(canvas)
        self.drawPieces(canvas)
        self.drawCheck(canvas)

        if self.machineLevel == None:
            canvas.create_text(1150, 670, text = "Select a difficulty level for the AI before moving (Digit between 0 and 3)")
        else: canvas.create_text(1150, 670, text = f'AI Difficulty is Level {self.machineLevel}', font = 'Arial 13')
        
        canvas.create_image(800, 100, image=ImageTk.PhotoImage(self.playerImage))
        canvas.create_image(1350, 100, image=ImageTk.PhotoImage(self.aiImage))
        canvas.create_rectangle(900, 0, 1275, 200, fill = 'honeydew')
        canvas.create_text(1050, 50, text = 'PLAYER', font = 'Arial 20 bold')
        canvas.create_text(1050, 100, text = 'VS', font = 'Arial 20 bold')
        canvas.create_text(1050, 150, text = 'AI', font = 'Arial 20 bold')
        
        canvas.create_text(850, 630, text = 'Key Commands Are:', font = 'Arial 18')
        canvas.create_text(1075, 630, text = '\'B\' to Return to Menu', font = 'Arial 13')
        canvas.create_text(1250, 630, text = '\'R\' to Restart Game', font = 'Arial 13')
        
        if self.gameOver == False:
            if self.turn == 'white': 
                canvas.create_text(950, 450, text = 'Your Turn!'
                                , font = 'Arial 20 bold')
            elif self.turn == 'black': 
                canvas.create_text(950, 450, text = 'AI Thinking'
                                , font = 'Arial 20 bold')
                
        canvas.create_text(1275, 430, text = f'Piece Placement Eval: {self.pieceEval}')
        canvas.create_text(1275, 470, text = f'Material Eval: {self.materialEval}')