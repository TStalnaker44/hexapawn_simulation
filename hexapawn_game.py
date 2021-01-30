
from hexapawn import Board, Bot

class Game():

    def __init__(self, n=3, learn = (True, True)):
        self._n = n
        self._board = Board(n)
        self._p1 = Bot()
        self._p2 = Bot()
        self._turn = 1
        self._gameOver = False
        self._gameCount = 0
        self._wins = {1:0, 2:0}
        self._learnSwitch = learn

    def reset(self):
        self._board = Board(self._n)
        self._gameOver = False
        self._turn = 1
        self._gameCount += 1

    def executeTurn(self):
        if self._turn % 2 == 1:
            move = self._p1.pickMove(self._turn,
                                     self._board.getBoardState())
        else:
            move = self._p2.pickMove(self._turn,
                                     self._board.getBoardState())
        if move == None:
            self._gameOver = True
            return 0 # Exit the method on losing state
        self._board.executeMove(move)
        self._turn += 1

    def isGameOver(self):
        self._gameOver = self._board.isGameOver(self._turn) or \
                         self._gameOver
        return self._gameOver

    def gameWrapUp(self):

        # Find the winner
        winner = self._board.getWinner(self._turn)
        if self._p1._forfeit:
            winner = 2
        if self._p2._forfeit:
            winner = 1

        # Reset bot forfeit states
        self._p1._forfeit = False
        self._p2._forfeit = False

        # Increment score board
        self._wins[winner] += 1

        # Train both models
        if self._learnSwitch[0]:
            self._p1.learn(winner==1)
        if self._learnSwitch[1]:
            self._p2.learn(winner==2)

    def trainModels(self, epochs=100):
        for x in range(epochs):
            while not self.isGameOver():
                self.executeTurn()
            self.gameWrapUp()
            self.reset()
        
