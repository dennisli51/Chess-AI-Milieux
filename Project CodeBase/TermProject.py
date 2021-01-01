# Dennis Li (AndrewId: dfli) Term Project 
############################################################################
import math, copy, random, time
from cmu_112_graphics import *
from pieces import *
from HumanBattle import *
from ManMachine import *
############################################################################
#Different Modal Apps and subclassing structure based on Animation Notes Part 3
    
class MachineBattle(ManMachine): 
    #AI vs AI Exhibition Mode. Remaining modes can be found in other files. 
         
    def appStarted(self):
        self.margin = 5
        self.gridHeight = self.gridWidth = self.height - 2*self.margin
        self.pressRow = None; self.pressCol = None
        self.setUpPieces()
        self.machineLevel = None #black's machine level (default AI)
        self.machineLevelWhite = None 
        self.pieceSquareTables()
        self.pieceEval = self.materialEval = 0
        self.aiText = None
        #image taken from online site
        self.aiURL = 'https://i.pinimg.com/originals/f0/2d/81/f02d81ee7d2ccd7c89ecf792f23e02c2.jpg'
        self.aiImage = self.scaleImage(self.loadImage(self.aiURL), 0.3)

    def timerFired(self):
        self.materialEval = self.boardEval(self.boardPieces, 'white')
        self.pieceEval = self.squareTableEval(self.boardPieces, 'white')
        self.constantlyCheck() 

    def mousePressed(self, event):
        if (self.pointInGrid(event.x, event.y) and (self.machineLevel == None or 
            self.machineLevelWhite == None or self.gameOver == True or 
            self.stalemate == True)):
            return

    def keyPressed(self, event):
        if (event.key == 'r'):
            self.setUpPieces()
            self.machineLevelWhite = self.machineLevel = None 
        elif (event.key == 'b'):
            self.app.setActiveMode(self.app.splashScreenMode)
        elif event.key.isdigit() and self.machineLevel == None and 0 <= int(event.key) < 4:
            self.machineLevel = int(event.key)
        elif event.key.isdigit() and self.machineLevelWhite == None and 0 <= int(event.key) < 4:
            self.machineLevelWhite = int(event.key)
        elif event.key == 'g':
            if (self.turn == 'black' and self.gameOver == False and self.machineLevel != None):
                self.botMove(self.machineLevel, 'black', self.boardPieces, self.boardView)
            elif self.turn == 'white' and self.gameOver == False and self.machineLevelWhite != None:
                self.botMove(self.machineLevelWhite, 'white', self.boardPieces, self.boardView)

    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,self.width,self.height, fill = 'lightgray') 
        canvas.create_rectangle(700, 500, 1400, 700, fill = 'honeydew')
        canvas.create_rectangle(700, 200, 1400, 500, fill = 'honeydew')
        canvas.create_rectangle(820, 0, 1275, 200, fill = 'silver')
        self.drawBoard(canvas)
        self.drawPieces(canvas)
        self.drawCheck(canvas)
            
        if self.machineLevel == None:
            canvas.create_text(1000, 525, text = 
            "Select a difficulty level for the Black AI before moving by pressing digit between 0-3")
        else: canvas.create_text(1150, 100, text = f'Black AI Difficulty Level {self.machineLevel}')
        if self.machineLevelWhite == None:
            canvas.create_text(1000, 550, text = 
            "Select a difficulty level for the White AI before moving by pressing digit between 0-3")
        else: canvas.create_text(950, 100, text = f'White AI Difficulty Level {self.machineLevelWhite}')
        
        if self.gameOver == False:
            if self.turn == 'white': 
                canvas.create_text(950, 450, text = 'White AI\'s Turn'
                                , font = 'Arial 20 bold')
            elif self.turn == 'black': 
                canvas.create_text(950, 450, text = 'Black AI\'s Turn'
                                , font = 'Arial 20 bold')
        
        canvas.create_text(1275, 430, text = f'Piece Placement Eval: {self.pieceEval}')
        canvas.create_text(1275, 470, text = f'Material Eval: {self.materialEval}')
        
        canvas.create_image(772, 100, image=ImageTk.PhotoImage(self.aiImage))
        canvas.create_image(1350, 100, image=ImageTk.PhotoImage(self.aiImage))
        canvas.create_text(1050, 50, text = 'AI Mode', font = 'Arial 20 bold')
        canvas.create_text(1050, 100, text = 'VS', font = 'Arial 20 bold')
        canvas.create_text(1050, 150, text = 'AI Mode', font = 'Arial 20 bold')
        
        canvas.create_text(850, 630, text = 'Key Commands Are:', font = 'Arial 18')
        canvas.create_text(1075, 630, text = '\'B\' to Return to Menu', font = 'Arial 15')
        canvas.create_text(1070, 665, text = '\'R\' to Restart Game', font = 'Arial 15')
        canvas.create_text(1300, 645, text = '\'G\' to make AI Move', font = 'Arial 15')
        
            
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.manMachine = ManMachine()
        app.machineBattle = MachineBattle()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 1000

app = MyModalApp(width=1400, height=700)
