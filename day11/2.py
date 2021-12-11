#!/usr/bin/python3
import time
import sys

YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
END = '\033[0m'
CLEARSCR = '\033[2J'

f = open("input","r")
# f = open("input.test","r")

octos=[]
octoflashed=[]
for l in f.readlines():
    octos.append([int(x) for x in l.strip()])
    octoflashed.append([False for x in l.strip()])

def octoprint(o,f):
    for rowInd,rowVal in enumerate(o):
        for colInd,colVal in enumerate(rowVal):
            c=RED
            if f[rowInd][colInd]:
                c=YELLOW
            print(f"{c}{colVal}{END}",end="")
        print("")
    print("")


def addFlash(o,f,rowInd,colInd):
    if f[rowInd][colInd]:
        return # Already flashed it, no point to add.
    else:
        o[rowInd][colInd] += 1
        if o[rowInd][colInd] > 9:
            f[rowInd][colInd] = True
            # Process our flash
            for x in [colInd+x for x in range(-1,2)]:
                for y in [rowInd+x for x in range(-1,2)]:
                    if x >=0 and y >= 0 and y < len(o) and x < len(o[0]): # Bounds check
                        addFlash(o,f,y,x)

def loop(o,f):
    # Add/Flash
    for rowInd,rowVal in enumerate(o):
        for colInd,colVal in enumerate(rowVal):
            addFlash(o,f,rowInd,colInd)
    # Decay
    for rowInd,rowVal in enumerate(o):
        for colInd,colVal in enumerate(rowVal):
            if o[rowInd][colInd] == 10:
                o[rowInd][colInd] = 0
    octoprint(octos,octoflashed)  
    # Count/Reset Flash Map
    flashes=0
    for rowInd,rowVal in enumerate(o):
        for colInd,colVal in enumerate(rowVal):
            if f[rowInd][colInd]:
                flashes+=1
                f[rowInd][colInd] = False
    if(flashes == 100 ):
        print("We are done - your part 2 answer/step-no is above...")
        sys.exit(0)
    return flashes

totalflashes=0
for iters in range(1000):
    print(f"{CLEARSCR}Step {iters+1}")
    flashes = loop(octos,octoflashed)
    totalflashes += flashes
    print(f"Flashes {flashes} Total {totalflashes}")
    # time.sleep(0.1)

print("Sorry - we didn't find an all-flash event - try more iterations?")