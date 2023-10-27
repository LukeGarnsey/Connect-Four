#!/usr/bin/env python
# coding: utf-8

# In[8]:


from colorama import init
init()
from colorama import Fore
boardWidth = 7
boardHeight = 6
wallSpace = "|"
emptySpace = "_"
piece = "O"
playerOneColor = Fore.RED
playerTwoColor = Fore.BLUE


def board_setup():
    board = []
    row = []
    for _ in range(boardWidth):
        row.append((emptySpace, 0))

    for _ in range(boardHeight):
        board.append([x for x in row])

    return board

    # board[0][0] = redPiece
    # board[0][1] = redPiece
    # board[0][6] = redPiece
    # board[1][1] = yellowPiece
    # board[0][4] = yellowPiece
    # board[0][3] = redPiece
    # board[1][2] = redPiece
    # board[1][3] = redPiece
    # board[2][3] = redPiece
    # board[3][3] = redPiece
    # board[2][1] = redPiece
    # board[3][1] = redPiece
    # board[3][4] = redPiece
    # board[4][1] = redPiece
    # board[5][1] = redPiece
    # board[4][2] = redPiece
    # board[2][4] = redPiece


# In[10]:


def display_board(board):
    index = boardHeight - 1
    for item in reversed(board):
        rowString = Fore.GREEN + wallSpace
        for loc in item:
            color = Fore.GREEN
            if loc[1] == 1:
                color = playerOneColor 
            elif loc[1] == 2:
                color = playerTwoColor
            rowString += color + loc[0]
            rowString += Fore.GREEN + wallSpace

        print(rowString)
        index -= 1

    finalRow = " "
    for index in range(boardWidth):
        finalRow += Fore.WHITE + str(index + 1)
        finalRow += " "
    print(finalRow)


# In[11]:


def get_input(board, player):
    value = ""
    color = playerOneColor if player == 1 else playerTwoColor
    inputText = color + "Player One " + Fore.WHITE + "Place " + color + "piece " + Fore.WHITE + "(1 - 7): "
    while(value.isdigit() == False):
        value = input(inputText)
        if value.isdigit() == False or int(value) > boardWidth or int(value) < 1:
            print("Not 1 - 7")
            value = ""
            continue
        if check_column(board, int(value) - 1) < 0:
            print("Column Full")
            value = ""
            continue

    return int(value) - 1

def check_column(board, index):
    for rowNum, row in enumerate(board):
        #print(row[index])
        if row[index][1] != 0:
            continue
        #print("Place at " + str(rowNum))
        return rowNum
    return -1


# In[12]:


def check_board_for_win(board, checkForPlayer):
    verticalSet = set()
    horizontalSet = set()
    diagUpSet = set()
    diagDownSet = set()
    for rowIndex, row in enumerate(board):
        for columnIndex, cell in enumerate(row):
            if cell[1] == checkForPlayer:
                checkUp, verticalSet = vertical_check(board, rowIndex, columnIndex, checkForPlayer, verticalSet)
                if len(checkUp) == 4:
                    # print("VertWIN {1} {0}".format(checkUp, checkFor))
                    return True
                
                checkRight, horizontalSet = horizontal_check(board, rowIndex, columnIndex, checkForPlayer, horizontalSet)
                if len(checkRight) == 4:
                    # print("HozWin {1} {0}".format(checkRight, checkFor))
                    return True

                checkDiagUp, diagUpSet = diagnal_up_check(board, rowIndex, columnIndex, checkForPlayer, diagUpSet)
                if len(checkDiagUp) == 4:
                    # print("DiagUpWin {1} {0}".format(checkDiagUp, checkFor))
                    return True

                checkDiagDown, diagDownSet = diagnal_down_check(board, rowIndex, columnIndex, checkForPlayer, diagDownSet)
                if len(checkDiagDown) == 4:
                    # print("DiagDownWin {1} {0}".format(checkDiagDown, checkFor))
                    return True
    
    return False

def vertical_check(board, rowIndex, columnIndex, checkFor, verticalSet):
    debugColumnIndex = columnIndex + 1
    matchList = [(rowIndex, debugColumnIndex)]
    if (rowIndex, debugColumnIndex) in verticalSet:
        #print("break vertical for duplicate check: {0}".format((rowIndex, debugColumnIndex)))
        return (matchList, verticalSet)
    verticalSet.add((rowIndex, debugColumnIndex))
    for i in range(3):
        if rowIndex + i + 1 >= boardHeight:
            break
        if board[rowIndex + i + 1][columnIndex][1] != checkFor:
            break
        matchList.append((rowIndex + 1 + i, debugColumnIndex))
        verticalSet.add((rowIndex + 1 + i, debugColumnIndex))
    
    return (matchList, verticalSet)

def horizontal_check(board, rowIndex, columnIndex, checkFor, horizontalSet):
    debugColumnIndex = columnIndex + 1
    matchList = [(rowIndex, debugColumnIndex)]
    if (rowIndex, debugColumnIndex) in horizontalSet:
        #print("break Horizontal for duplicate check: {0}".format((rowIndex, debugColumnIndex)))
        return (matchList, horizontalSet)
    horizontalSet.add((rowIndex, debugColumnIndex))
    for i in range(3):
        if columnIndex + i + 1 >= boardWidth:
            break
        if board[rowIndex][columnIndex + i + 1][1] != checkFor:
            break
        matchList.append((rowIndex, debugColumnIndex+ i + 1))
        horizontalSet.add((rowIndex, debugColumnIndex+ i + 1))
    
    return (matchList, horizontalSet)

def diagnal_up_check(board, rowIndex, columnIndex, checkFor, listSet):
    debugColumnIndex = columnIndex + 1
    matchList = [(rowIndex, debugColumnIndex)]
    if (rowIndex, debugColumnIndex) in listSet:
        #print("break Diag Up for duplicate check: {0}".format((rowIndex, debugColumnIndex)))
        return (matchList, listSet)
    listSet.add((rowIndex, debugColumnIndex))
    for i in range(3):
        if columnIndex + i + 1 >= boardWidth or rowIndex + i + 1 >= boardHeight:
            break
        if board[rowIndex + i + 1][columnIndex + i + 1][1] != checkFor:
            break
        matchList.append((rowIndex + i + 1, debugColumnIndex + i + 1))
        listSet.add((rowIndex + i + 1, debugColumnIndex + i + 1))
    
    return (matchList, listSet)

def diagnal_down_check(board, rowIndex, columnIndex, checkFor, listSet):
    debugColumnIndex = columnIndex + 1
    matchList = [(rowIndex, debugColumnIndex)]
    if (rowIndex, debugColumnIndex) in listSet:
        #print("break Diag Down for duplicate check: {0}".format((rowIndex, debugColumnIndex)))
        return (matchList, listSet)
    listSet.add((rowIndex, debugColumnIndex))
    for i in range(3):
        if columnIndex + i + 1 >= boardWidth or rowIndex - i - 1 < 0:
            break
        if board[rowIndex - i - 1][columnIndex + i + 1][1] != checkFor:
            break
        matchList.append((rowIndex - i - 1, debugColumnIndex + i + 1))
        listSet.add((rowIndex - i - 1, debugColumnIndex + i + 1))
    
    return (matchList, listSet)


# In[13]:


def player_take_turn(board, player):
    columnIndex = get_input(board, player)
    rowIndex = check_column(board, columnIndex)
    board[rowIndex][columnIndex] = (piece, player)


# In[14]:


from IPython.display import clear_output
import time
gameActive = True
isPlayerOne = True
board = board_setup()
count = 0

while(gameActive):
    playerTurn = 1 if isPlayerOne else 2
    time.sleep(.1)
    display_board(board)
    player_take_turn(board, playerTurn)
    clear_output()
    count += 1
    isWin = check_board_for_win(board, playerTurn)
    if isWin or count == 42:
        display_board(board)
        if isWin == False:
            print("Game is a DRAW.")
        elif isPlayerOne:
            print(playerOneColor + "Player One Wins!")
        else:
            print(playerTwoColor + "Player Two Wins!")
        time.sleep(.15)
        value = ""
        while(value.upper() != "Y" and value.upper() != "N"):
            value = input("PLay Again? (N or Y)")

        if value.upper() == "N":
            gameActive = False
        else:
            board = board_setup()
            isPlayerOne = True
            count = 0
            clear_output()
    else:
        isPlayerOne = not isPlayerOne

print("Goodbye!")

