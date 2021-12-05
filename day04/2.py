#!/usr/bin/python3 
import re
import sys
from array import *

f = open("input","r")
# f = open("input.test","r")

# Read a single board from the given file object
def readBoard(f):
    board=[]
    blank=f.readline()
    if (blank != "\n"):
        print("Found non-start line",blank)
        return None
    else:
        for y in range(5):
            row = [ int(v) for v in re.split('\s+',f.readline().strip())]
            board.append(row)
        print(board)
    return board

# Play a bingo number on all boards - use '-1' for a marker.
def playNumber(boards,num):
    for board in range(len(boards)):
        # print("b",board)
        for row in range(len(boards[board])):
            # print("r",row)
            for col in range(len(boards[board][row])):
                if(boards[board][row][col] == num):
#                    print("Match in board,row,col",board,row,col)
                    boards[board][row][col] = -1         

def checkWins(boards,num):

    print("Checkwins for {} boards".format(len(boards)))

    winningboards=[]
    
    for board in range(len(boards)):
        boardWins=False
        # Horiz
        for row in range(len(boards[board])):
            rowWins=True
            for col in range(len(boards[board][row])):
                if boards[board][row][col] != -1:
                    rowWins = False
            if rowWins:
                print('Winner[ROW] board number {} row {}'.format(board,row))
                calculateWin(boards[board],num)
                boardWins=True
        # Vert 
        for col in range(len(boards[board][0])):
            colWins=True
            for row in range(len(boards[board])):
                if boards[board][row][col] != -1:
                    colWins = False
            if colWins:
                print('Winner[COL] board number {} col {}'.format(board,col))
                calculateWin(boards[board],num)
                boardWins=True

        if boardWins:
            winningboards.insert(0,board)

    # Now remove all winning boards - _outside_ the loop,so we don't clobber ourselves...
    print("Deleting WinningBoards",winningboards)
    for b in winningboards:
        del boards[b]
    if len(boards) == 0:
        print("The last winning board/score is ^^")
        sys.exit()
      
def calculateWin(board,num):   
    print("Winning Board",board)
    s=0
    for row in board:
        for col in row:
            if col != -1:
                s=s+col
    print("Sum {} * Num {} = {} ".format(s,num,s*num))

drawnumbers = [ int(x) for x in f.readline().strip().split(',')]

print(drawnumbers)

boards=[]
more=True
while(more):
    more = readBoard(f)
    if(more):
        boards.append(more)

print("Starting Boards",boards)
for num in drawnumbers:
    print("Playing number", num)
    playNumber(boards,num)
    checkWins(boards,num)
    # print("Boards ", boards)


