"""
Board State represented as a string
 0 = Blank Space
 1 = Player One
 2 = Player Two

 Moves represented as (from, to)

"""

import pprint, random, math

class Bot():

    def __init__(self):
        self._brain = {}#createStateMapping()
        self._lastMove = None
        self._moveMemory = []
        self._forfeit = False

        self._reward = True
        self._punish = True
        self._longTermMemory = True

    def usePunish(self, punish):
        self._punish = punish

    def useReward(self, reward):
        self._reward = reward
        
    def useLongTermMemory(self, mem):
        self._longTermMemory = mem

    def pickMove(self, turn, state):
        # Allow the bot to learn the moves naturally
        if not turn in self._brain:
            self._brain[turn] = {}
        if not state in self._brain[turn]:
            self._brain[turn][state] = getMoves(state, turn)
        possibleMoves = self._brain[turn][state]
        if possibleMoves == []:
            self._forfeit = True
            self._lastMove = None
            return None #The bot forfeits in losing state
        move = random.choice(possibleMoves)
        self._lastMove = (turn, state, move)
        self._moveMemory.append(self._lastMove)
        return move

    def learn(self, won):
        if self._lastMove != None:
            turn, state, move = self._lastMove
            if won:
                if self._reward:
                    if self._longTermMemory:
                        for memory in self._moveMemory:
                            turn, state, move = memory
                            for x in range(3):
                                self._brain[turn][state].append(move)
                        self._moveMemory = []
                    else:
                        for x in range(3):
                            self._brain[turn][state].append(move)
                        self._moveMemory = []
            else:
                if self._punish:
                    self._brain[turn][state].remove(move)
        
class Board():

    def __init__(self, n=3):
        self._n = n
        encoding = ("2"*n) + ("0"*n*(n-2)) + ("1"*n)
        self._board = [c for c in encoding]

    def getBoardState(self):
        return "".join(self._board)

    def executeMove(self, move):
        self._board[move[1]] = self._board[move[0]]
        self._board[move[0]] = "0"

    def printBoard(self):
        n = self._n
        state = self.getBoardState()
        state = state.replace("2", "X")
        state = state.replace("1", "O")
        state = state.replace("0", " ")
        output = "\n".join(state[n*x:n*(x+1)]
                           for x in range(n))
        print(output)

    def isGameOver(self, turn):
        n = self._n
        if not "2" in self._board or \
           not "1" in self._board or \
           "2" in self._board[(n*n)-n:n*n] or \
           "1" in self._board[0:n] or \
           getMoves(self.getBoardState(), turn) == []:
            return True
        else:
            return False

    def getWinner(self, turn):
        n = self._n
        if "1" in self._board[0:self._n]:
            return 1
        if "2" in self._board[(n*n)-n:n*n]:
            return 2
        if not "2" in self._board:
            return 1
        if not "1" in self._board:
            return 2
        if getMoves(self.getBoardState(), turn) == []:
            return ((turn) % 2)+1

def getMoves(state, turn):
    moves = []
    n = int(math.sqrt(len(state)))
    for x, piece in enumerate(state):

        #Handle Player 2
        if piece == "2" and turn % 2 == 0:
            targetRow = (x//n)+1
            start = targetRow * n
            indices = [i for i in range(start, start+n)]
            # Check the first column
            if x%n == 0:
                if state[indices[0]] == "0":
                    moves.append((x,indices[0]))
                if state[indices[1]] == "1":
                    moves.append((x,indices[1]))
            # Check the last column
            elif x%n == n-1:
                if state[indices[n-2]] == "1":
                    moves.append((x,indices[n-2]))
                if state[indices[n-1]] == "0":
                    moves.append((x,indices[n-1]))
            # Check other columns
            else:
                if state[indices[x%n-1]] == "1":
                    moves.append((x,indices[x%n-1]))
                if state[indices[x%n]] == "0":
                    moves.append((x,indices[x%n]))
                if state[indices[x%n+1]] == "1":
                    moves.append((x,indices[x%n+1]))
            

        # Handle Player 1            
        if piece == "1" and turn % 2 == 1:
            targetRow = (x//n)-1
            start = targetRow * n
            indices = [i for i in range(start, start+n)]
            # Check the first column
            if x%n == 0:
                if state[indices[0]] == "0":
                    moves.append((x,indices[0]))
                if state[indices[1]] == "2":
                    moves.append((x,indices[1]))
            # Check the last column
            elif x%n == n-1:
                if state[indices[n-2]] == "2":
                    moves.append((x,indices[n-2]))
                if state[indices[n-1]] == "0":
                    moves.append((x,indices[n-1]))
            # Check other columns
            else:
                if state[indices[x%n-1]] == "2":
                    moves.append((x,indices[x%n-1]))
                if state[indices[x%n]] == "0":
                    moves.append((x,indices[x%n]))
                if state[indices[x%n+1]] == "2":
                    moves.append((x,indices[x%n+1]))

    return moves

def simulate(silent=False):

    print("Training Model...")

    games = 1
    
    HIM = Bot()
    HER = Bot()

    wins = {1:0, 2:0}

    for x in range(games):
        
        board = Board(4)
        turn = 1

        if not silent:
            print("Turn: 0")
            board.printBoard()

        while not board.isGameOver(turn):
            if not silent:
                print("Turn:", turn)
            if turn % 2 == 1:
                move = HIM.pickMove(turn, board.getBoardState())
            else:
                move = HER.pickMove(turn, board.getBoardState())
            if move == None:
                break
            print(move)
            board.executeMove(move)
            if not silent:
                board.printBoard()
            turn += 1

        winner = board.getWinner(turn)
        if HIM._forfeit:
            winner = 2
        if HER._forfeit:
            winner = 1
        #HIM.learn(winner==1)
        HER.learn(winner==2)
        if not silent:
            print("Player %d won the game" % (winner))

        HIM._forfeit = False
        HER._forfeit = False

        wins[winner] += 1

    print("HIM wins:", wins[1])
    print("HER wins:", wins[2])
    print("Of", games, "games")
    
    print("\nModel Trained!\n")

    interactiveGame(HER)

def interactiveGame(bot):

    while True:
    
        board = Board()
        turn = 1
        
        while not board.isGameOver(turn):
            if turn % 2 == 1:
                print("Your Turn")
                board.printBoard()
                move = input("What is your move? ")
                move = (int(move[0]), int(move[1]))
            else:
                print("The bot's turn")
                board.printBoard()
                move = bot.pickMove(turn, board.getBoardState())
            if move == None:
                break
            board.executeMove(move)
            
            turn += 1
            
        board.printBoard()
        winner = board.getWinner(turn)
        if bot._forfeit:
            winner = 1
        bot.learn(winner==2)
        print("Player %d won the game" % (winner))

        bot._forfeit = False

        again = input("Play again? (y/n) ")
        if again.lower() == "n": break
    
if __name__=="__main__":
    simulate()

    
