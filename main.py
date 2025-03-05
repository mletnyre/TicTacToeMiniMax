import random
import re

def translateToZeroIndex(x, y):
    return x-1, y-1

def placePiece(x, y, board, c):
    board[y][x] = c

def validSpot(x, y, board):
    if board[y][x] == '-':
        return True
    return False

def printBoard(board):
    for row in board:
        print(row)

def nextTurn(turn, human, computer):
    if turn == human:
        return computer
    elif turn == computer:
        return human
    
def getValidInput(board):
    while True:
        print("Enter the position you would like to place an x in (please enter it in the format x y)")
        inpt = input()
        if re.match(r'^[1-3] [1-3]$', inpt):
            x, y = map(int, inpt.split())
            x, y = translateToZeroIndex(x, y)
            if(validSpot(x, y, board)):
                return x, y
           
        print("Enter the position you would like to place an x in (please enter it in the format x y), it is sensitive about spaces at the end")

    
def humanTurn(board, human):
    x,y = getValidInput(board)
    placePiece(x,y, board, human)

def naiveComputerTurn(board, computer):
    x = random.randint(0,2)
    y = random.randint(0,2)
    while(not validSpot(x,y,board)):
        x = random.randint(0,2)
        y = random.randint(0,2)
    placePiece(x,y,board,computer)


def minimax(board,maximizingPlayer):
    if maximizingPlayer:
        cur = 'o'
        oth = 'x'
    if not maximizingPlayer:
        cur = 'x'
        oth = 'o'

    #returns true if cur has a winning 3 in some spot on the board
    result = checkWin(board, oth)
    if result == 1 and maximizingPlayer:
        return -1 #return 1 beacuse this is the best possible outcome
    elif result == 0 and not maximizingPlayer: 
        return 1 #return -1 because this is the worst possible outcome
    elif result == 2: #results == 2 when it is a tie this is a 0 value
        return 0
    if maximizingPlayer:
        best = -99999
        for x in range(3):
            for y in range(3):
                if board[y][x] == '-':
                    board[y][x] = cur
                    score = minimax(board, False)
                    board[y][x] = '-'
                    best = max(score, best)
        return best
    if not maximizingPlayer:
        best = 99999
        for x in range(3):
            for y in range(3):
                if board[y][x] == '-':
                    board[y][x] = cur
                    score = minimax(board, True)
                    board[y][x] = '-'
                    best = min(score, best)
        return best




def computerTurnMiniMax(board, computer):
    bestScore = -999999999
    #look at every possible move and try it
    for x in range(3):
        for y in range(3):
            if board[y][x] == '-':
                #get the score from this board
                board[y][x] = computer
                score = minimax(board, False)
                board[y][x] = '-'
                if score > bestScore:
                    bestScore = score
                    bestX = x
                    bestY = y
    placePiece(bestX,bestY,board,computer)
    

def tie(board):
    for x in range(3):
        for y in range(3):
            if board[y][x] == '-':
                return False
    return True


def horzWin(board, turn):
    for row in board:
        if row[0] == row[1] and row[0] == row[2] and row[0] == turn and row[1] == turn and row[2] == turn:
            return True
    return False

def virWin(board, turn):
    tmpbd = list(zip(*board)) #zip flips the rows a cols
    for row in tmpbd:
        if row[0] == row[1] and row[0] == row[2] and row[0] == turn and row[1] == turn and row[2] == turn:
            return True
    return False

def diagWin(board, turn):
    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] == turn and board[1][1] == turn and board[2][2] == turn:
        return True
    elif board[2][0] == board[1][1] and board[2][0] == board[0][2] and board[0][0] == turn and board[0][2] == turn and board[2][0] == turn:
        return True
    return False

def checkWin(board, turn):
    if (horzWin(board, turn) or virWin(board, turn) or diagWin(board, turn)) and turn == 'o':
        return 0
    elif (horzWin(board, turn) or virWin(board, turn) or diagWin(board, turn)) and turn == 'x':
        return 1
    elif tie(board):
        return 2

def main():
    board = [
        ['-','-','-'],
        ['-','-','-'],
        ['-','-','-']
    ]
    human = 'x'
    computer = 'o'
    turn = computer #start with computer turn since we switch the turn at the begining of each loop

    winner = False

    while(not winner):
        printBoard(board)
        print("\n")
        turn = nextTurn(turn, human, computer)
        if turn == human:
            humanTurn(board, human)
        elif turn == computer:
            computerTurnMiniMax(board, computer)

        winner = checkWin(board, turn)

    if winner == 1 or winner == 0:
        print("we found a winner")
    elif winner == 2:
        print("TIE")


    printBoard(board)

if __name__ == "__main__":
    main()