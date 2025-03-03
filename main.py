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

def isBoardFull(board):
    for row in board:
        if row[0] == '-' or row[1] == '-' or row[2] == '-':
            return False
    
    return True

def evaluateBoard(board):
    return 1

def minimax(board, depth, maximizingPlayer):
    if maximizingPlayer:
        cur = 'x'
    if not maximizingPlayer:
        cur = 'o'
    result = checkWin(board, cur)
    if result == True and maximizingPlayer:
        return 1
    elif result == True and not maximizingPlayer:
        return -1

    if maximizingPlayer:
        best = -99999
        for x in range(3):
            for y in range(3):
                if board[y][x] == '-':
                    score = minimax(board, depth + 1, False)
                    board[y][x] = '-'
                    best = max(score, best)
        return best
    if not maximizingPlayer:
        best = 99999
        for x in range(3):
            for y in range(3):
                if board[y][x] == '-':
                    score = minimax(board, depth + 1, True)
                    board[y][x] = '-'
                    best = max(score, best)
        return best




def computerTurnMiniMax(board, computer):
    bestScore = -999999999
    for x in range(3):
        for y in range(3):
            if board[y][x] == '-':
                score = minimax(board, 0, False)
                board[y][x] = '-'
                if score > bestScore:
                    bestScore = score
                    bestX = x
                    bestY = y
    placePiece(bestX,bestY,board,computer)
    

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
    return horzWin(board, turn) or virWin(board, turn) or diagWin(board, turn)


def main():
    board = [
        ['-','-','-'],
        ['-','-','-'],
        ['-','-','-']
    ]
    human = 'x'
    computer = 'o'
    turn = computer
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
        
    print("we found a winner")
    printBoard(board)

if __name__ == "__main__":
    main()