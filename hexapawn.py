"""
Board State represented as a string
 0 = Blank Space
 1 = Player One
 2 = Player Two

 Moves represented as (from, to)

"""

import pprint, random

states = {1:["222000111"],
          2:["222001110",
             "222010101"],
          3:["202200011",
             "202120011",
             "220102011",
             "022210101",
             "022020101"],
          4:["022211100",
             "202201010",
             "202210001",
             "220101001",
             "202100001",
             "022021100",
             "022120001",
             "220112001",
             "202110010",
             "022010100",
             "022010001"],
          5:["002220001",
             "200220001",
             "200212001",
             "002120010",
             "020012100",
             "200112010",
             "020122001",
             "200212001",
             "200201001",
             "200121001",
             "020020001"],
          6:["200111000",
             "002221000",
             "200221000",
             "020021000",
             "002210000",
             "020112000",
             "200210000"],
          7:["000212000",
             "000121000",
             "000211000",
             "000021000"]}

class Bot():

    def __init__(self):
        self._brain = createStateMapping()
        self._memory = []

    def pickMove(self, turn, state):
        possibleMoves = self._brain[turn][state]
        move = random.choice(possibleMoves)
        self._memory.append((turn, state, move))
        return move

    def learn(self, won):
        ## Allow a toggle for this
        ## Increase number of good moves
        ## Decrease the number of bad moves
        pass

class Board():

    def __init__(self):
        self._board = [c for c in "222000111"]

    def getBoardState(self):
        return "".join(self._board)

    def executeMove(self, move):
        self._board[move[1]] = self._board[move[0]]
        self._board[move[0]] = "0"

    def printBoard(self):
        print(getStateVisualization(self.getBoardState()))

    def isGameOver(self, turn):
        if not "2" in self._board or \
           not "1" in self._board or \
           "2" in self._board[6:9] or \
           "1" in self._board[0:3] or \
           getMoves(self.getBoardState(), turn) == []:
            return True
        else:
            return False

def getStateVisualization(state):
    state = state.replace("2", "X")
    state = state.replace("1", "O")
    state = state.replace("0", " ")
    return f"{state[:3]}\n{state[3:6]}\n{state[6:]}"

def mirrorState(state):
    firstrow = state[0:3][::-1]
    secondrow = state[3:6][::-1]
    thirdrow = state[6:9][::-1]
    return firstrow + secondrow + thirdrow

def getMoves(state, turn):
    moves = []
    for x, piece in enumerate(state):

        #Handle Player 2
        if piece == "2" and turn % 2 == 0:
            targetRow = (x//3)+1
            start = targetRow * 3
            indices = [i for i in range(start, start+3)]
            # Check the first column
            if x%3 == 0:
                if state[indices[0]] == "0":
                    moves.append((x,indices[0]))
                if state[indices[1]] == "1":
                    moves.append((x,indices[1]))
            # Check the second column
            elif x%3 == 1:
                if state[indices[0]] == "1":
                    moves.append((x,indices[0]))
                if state[indices[1]] == "0":
                    moves.append((x,indices[1]))
                if state[indices[2]] == "1":
                    moves.append((x,indices[2]))
            # Check the third column
            elif x%3 == 2:
                if state[indices[1]] == "1":
                    moves.append((x,indices[1]))
                if state[indices[2]] == "0":
                    moves.append((x,indices[2]))

        # Handle Player 1            
        if piece == "1" and turn % 2 == 1:
            targetRow = (x//3)-1
            start = targetRow * 3
            indices = [i for i in range(start, start+3)]
            # Check the first column
            if x%3 == 0:
                if state[indices[0]] == "0":
                    moves.append((x,indices[0]))
                if state[indices[1]] == "2":
                    moves.append((x,indices[1]))
            # Check the second column
            elif x%3 == 1:
                if state[indices[0]] == "2":
                    moves.append((x,indices[0]))
                if state[indices[1]] == "0":
                    moves.append((x,indices[1]))
                if state[indices[2]] == "2":
                    moves.append((x,indices[2]))
            # Check the third column
            elif x%3 == 2:
                if state[indices[1]] == "2":
                    moves.append((x,indices[1]))
                if state[indices[2]] == "0":
                    moves.append((x,indices[2]))
    return moves

def createStateMapping():
    states2moves = dict()
    # Create a mapping from states to moves
    for turn, stateLyst in states.items():
        for state in stateLyst:
            if turn in states2moves.keys():
                states2moves[turn][state] = getMoves(state, turn)
            else:
                states2moves[turn] = {state : getMoves(state, turn)}
            mirroredState = mirrorState(state)
            if not mirroredState in stateLyst:
                states2moves[turn][mirroredState] = getMoves(mirroredState, turn)
    return states2moves



board = Board()
HIM = Bot()
HER = Bot()
turn = 1

while not board.isGameOver(turn):
    print("Turn:", turn)
    board.printBoard()
    if turn % 2 == 1:
        move = HIM.pickMove(turn, board.getBoardState())
    else:
        move = HER.pickMove(turn, board.getBoardState())
    board.executeMove(move)
    turn += 1

  

    
