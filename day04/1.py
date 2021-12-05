#!/usr/bin/python3 
import re
import sys
from array import *


f = open("input","r")
# f = open("input.test","r")



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

def playNumber(boards,num):
    for board in range(len(boards)):
        # print("b",board)
        for row in range(len(boards[board])):
            # print("r",row)
            for col in range(len(boards[board][row])):
                if(boards[board][row][col] == num):
                    print("Match in board,row,col",board,row,col)
                    boards[board][row][col] = -1         


def checkWins(boards,num):
    # Horiz
    for board in range(len(boards)):
        for row in range(len(boards[board])):
            rowWins=True
            for col in range(len(boards[board][row])):
                if boards[board][row][col] != -1:
                    rowWins = False
            if rowWins:
                print('Winner board number {} row {} sum {}'.format(board,row,sum))
                calculateWin(boards[board],num)

def calculateWin(board,num):   
    print("Winning Board",board)
    sum=0
    for row in board:
        for col in row:
            if col != -1:
                sum=sum+col
    print("Sum {} * Num {} = {} ".format(sum,num,sum*num))

    sys.exit()

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
    print("Boards ", boards)


