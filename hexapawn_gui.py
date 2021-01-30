"""
Author: Trevor Stalnaker
File: queens_gui.py
"""

import pygame, time, random
from hexapawn import Bot, Board
TILE_WIDTH = 50
WHITEPAWN = pygame.image.load("pawn_white.png")
BLACKPAWN = pygame.image.load("pawn_black.png")

class HexapawnGUI():

    def __init__(self, n=3):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Checker Board GUI')
        self._n = n
        dim = TILE_WIDTH * n #pixelsPerSquare * (numSquares + padding)
        self._screen = pygame.display.set_mode((dim+20,dim+90))

        # Make the pawn image transparent
        global WHITEPAWN
        WHITEPAWN = WHITEPAWN.convert()
        WHITEPAWN.set_colorkey(WHITEPAWN.get_at((0,0)))

        global BLACKPAWN
        BLACKPAWN = BLACKPAWN.convert()
        BLACKPAWN.set_colorkey(BLACKPAWN.get_at((0,0)))

##        self.makeButtons()
##        self.makeInstructions()
        
        self._RUNNING = True
        self._board = Board(self._n)
        self.makeBoard()
##        self._solved = False
##        self._animating = False
##        self._waitForPlayer = False

##    def makeButtons(self):
##        y = (TILE_WIDTH * self._n) + 50
##        self._newButton = Button((100, y), "New")
##        x = self._newButton.getWidth() + self._newButton._pos[0] + 10
##        self._quickSolveButton = Button((x, y), "Quick Solve")
##        x = self._quickSolveButton.getWidth() + \
##            self._quickSolveButton._pos[0] + 10
##        self._stepSolveButton = Button((x, y), "Step Solve")

##    def makeInstructions(self):
##        font = pygame.font.SysFont("Times New Roman", 16)
##        self._instructions = font.render("Place a Queen Above", True, (0,0,0))
  
##    def quickSolve(self):
##        self._solved = True
##        self._board.solve()
##        self.makeBoard()
        
##    def animatedSolve(self):
##        self._animating = True
##        start_new_thread(self._solve, ())
##
##    def _solve(self):
##        self._board.solve(self.animate)
##        self.makeBoard()
##        self._solved = True

##    def animate(self):
##        if self._animating:
##            self.makeBoard()
##            time.sleep(.5)

    def makeBoard(self):
        tiles = []
        for i in range(self._n):
            for j in range(self._n):
                x = (TILE_WIDTH * (j)) + 10
                y = (TILE_WIDTH * (i)) + 10
                if i%2 == j%2:
                    color = (255,0,0)
                else:
                    color = (0,0,0)
                index = (self._n * i) + j
                pawn = self._board.getBoardState()[index]
                tiles.append(BoardTile((x,y),color, pawn))
        self._tiles = tiles
        
    def draw(self):
        self._screen.fill((230,230,230))
        for t in self._tiles:
            t.draw(self._screen)
        
##        self._newButton.draw(self._screen)
##        self._quickSolveButton.draw(self._screen)
##        self._stepSolveButton.draw(self._screen)
##        if self._waitForPlayer:
##            self._screen.blit(self._instructions, (142,420))
        pygame.display.flip()

    def handleEvents(self): 
        for event in pygame.event.get():
            
            if (event.type == pygame.QUIT):
                self._RUNNING = False

            ## Handle events on the solve buttons
##            self._stepSolveButton.handleEvent(event, self.solveAnimated)
##            self._quickSolveButton.handleEvent(event, self.solveQuick)

            ## Keyboard Short-cut for a new board          
##            if event.type == pygame.KEYDOWN and \
##               event.key == pygame.K_n:
##                self.newBoard()

            ## Button press for a new board
##            self._newButton.handleEvent(event, self.newBoard)

            ## Allow the player to place a new queen on the board
##            if self._waitForPlayer:
##                if event.type == pygame.MOUSEBUTTONDOWN and \
##                   event.button == 1 and event.pos[1] < 8*TILE_WIDTH + 10:
##                    x, y = event.pos
##                    column = (x - 10)  // TILE_WIDTH
##                    row = (y - 10) // TILE_WIDTH
##                    self._board.placeQueen(row, column)
##                    self.makeBoard()
##                    self._waitForPlayer = False

    def newBoard(self):
        self._board = Board(None)
        self.makeBoard()
        if self._animating:
            self._animating = False
            #Allow the other thread to terminate
            time.sleep(.25) 
        self._solved = False
        self._waitForPlayer = True

    def solveAnimated(self):
        if not self._solved:
            self.animatedSolve()

    def solveQuick(self):
        if not self._solved:
            if not self._animating:
                self.quickSolve()
            else:
                self._animating = False
                    
    def runGameLoop(self):
        while self.isRunning():
            self.draw()
            self.handleEvents()
        pygame.quit()

    def isRunning(self):
        return self._RUNNING

class BoardTile():

    def __init__(self, pos, color, pawn=0):
        self._pos = pos
        self._image = pygame.Surface((TILE_WIDTH,TILE_WIDTH))
        self._image.fill(color)
        if int(pawn):
            x_pos = (TILE_WIDTH // 2) - (BLACKPAWN.get_width() // 2)
            y_pos = (TILE_WIDTH // 2) - (BLACKPAWN.get_height() // 2)
            if int(pawn) == 1:
                self._image.blit(WHITEPAWN, (x_pos,y_pos))
            else:
                self._image.blit(BLACKPAWN, (x_pos,y_pos))

    def draw(self, screen):
        screen.blit(self._image, self._pos)

class Button():

    def __init__(self, pos, text, onclick=None):

        self._pos = pos
        
        font = pygame.font.SysFont("Times New Roman", 16)
        t = font.render(text, True, (0,0,0))
        padding = 6
        dims = (t.get_width() + padding, t.get_height() + padding)
        self._image = pygame.Surface(dims)
        self._image.fill((120,120,120))  
        self._image.blit(t, (padding//2,padding//2))

    def draw(self, screen):
        screen.blit(self._image, self._pos)

    def handleEvent(self, event, func):
        rect = self._image.get_rect()
        rect = rect.move(*self._pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(event.pos):
                func()

    def getWidth(self):
        return self._image.get_width()


g = HexapawnGUI(3)
g.runGameLoop()
