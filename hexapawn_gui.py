"""
Author: Trevor Stalnaker
File: queens_gui.py
"""

import pygame, time, random
from hexapawn_game import Game
TILE_WIDTH = 75
WHITEPAWN = pygame.image.load("pawn_white.png")
BLACKPAWN = pygame.image.load("pawn_black.png")

def main():
    n = 5
    bot1Learns = True
    bot2Learns = True
    trainingEpochs = 50000
    g = HexapawnGUI(n, (bot1Learns, bot2Learns), trainingEpochs)
    g.runGameLoop()
    
class HexapawnGUI():

    def __init__(self, n=3, learning=(True, True), epochs=0):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Checker Board GUI')
        self._n = n
        dim = TILE_WIDTH * n #pixelsPerSquare * (numSquares + padding)
        self._screen = pygame.display.set_mode((dim+20,dim+90))

        self._gameClock = pygame.time.Clock()
        self._moveTime = .05
        self._moveTimer = self._moveTime

        self._font = pygame.font.SysFont("Times New Roman", 16)

        # Make the pawn image transparent
        global WHITEPAWN
        WHITEPAWN = WHITEPAWN.convert()
        WHITEPAWN.set_colorkey(WHITEPAWN.get_at((0,0)))

        global BLACKPAWN
        BLACKPAWN = BLACKPAWN.convert()
        BLACKPAWN.set_colorkey(BLACKPAWN.get_at((0,0)))
        
        self._RUNNING = True
        self._g = Game(self._n, learning)
        self.setBotParams()
        self._g.trainModels(epochs)
        self.makeBoard()

    def setBotParams(self):
        p1 = self._g._p1
        p1.usePunish(True)
        p1.useReward(False)
        p1.useLongTermMemory(True)
        p2 = self._g._p2
        p2.usePunish(True)
        p2.useReward(False)
        p2.useLongTermMemory(True)

    def makeBoard(self):
        tiles = []
        board = self._g._board
        for i in range(self._n):
            for j in range(self._n):
                x = (TILE_WIDTH * (j)) + 10
                y = (TILE_WIDTH * (i)) + 10
                if i%2 == j%2:
                    color = (255,0,0)
                else:
                    color = (0,0,0)
                index = (self._n * i) + j
                pawn = board.getBoardState()[index]
                tiles.append(BoardTile((x,y),color, pawn))
        self._tiles = tiles
        
    def draw(self):
        self._screen.fill((230,230,230))
        for t in self._tiles:
            t.draw(self._screen)
        self.drawScoreBoard()
        pygame.display.flip()

    def drawScoreBoard(self):
        # Draw total games played
        played = self._font.render(("Games Played: %d" % (self._g._gameCount)),
                                   True, (0,0,0))
        x_coord = self._screen.get_width()//2 - played.get_width()//2
        y_coord = TILE_WIDTH * (self._n+.25)
        self._screen.blit(played,(x_coord,y_coord))

        # Draw player win totals
        for x in range(1,3):
            wins = self._font.render(("Player %d Wins: %d" % (x, self._g._wins[x])),
                                   True, (0,0,0))
            x_coord = self._screen.get_width()//2 - wins.get_width()//2
            y_coord =y_coord + 25
            self._screen.blit(wins,(x_coord,y_coord))

    def handleEvents(self): 
        for event in pygame.event.get():
            
            if (event.type == pygame.QUIT):
                self._RUNNING = False

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
            self._gameClock.tick()
            self.draw()
            self.handleEvents()
            self.update()
        pygame.quit()

    def isRunning(self):
        return self._RUNNING

    def update(self):
        ticks = self._gameClock.get_time() / 1000
        if not self._g.isGameOver():
            if self._moveTimer < 0:
                self._g.executeTurn()
                self.makeBoard()
                self._moveTimer = self._moveTime
            else:
                self._moveTimer -= ticks
        else:
            self._g.gameWrapUp()
            self._g.reset()
            self.makeBoard()
            self._moveTimer = self._moveTime

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


if __name__=="__main__":
    main()
