#!/usr/bin/python3
import time

YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
END = '\033[0m'
CLEARSCR = '\033[2J'

class Cave:
    def __init__(self, name):
        self.name = name
        self.isVisited = False
        self.isLarge = False
        if name.upper() == name:
            self.isLarge = True
        self.adjacents = []
    def __str__(self):
        return f"Cave[{self.name} L:{self.isLarge} V:{self.isVisited}]"
    def __repr__(self):
        return f"Cave[{self.name} L:{self.isLarge} V:{self.isVisited}]"
    def addAdjacent(self,cave):
        self.adjacents.append(cave)

def readNodes(fn):
    f = open(fn,"r")
    for line in f:
        print(f"Processing {line.strip()}")
        elems = [ x for x in line.strip().split('-')]
        for cave in elems:
            if cave in caves:
                print(f"Already exists - Not adding {cave}")
            else:
                caves[cave] = Cave(cave)
        caves[elems[0]].addAdjacent(caves[elems[1]])
        caves[elems[1]].addAdjacent(caves[elems[0]])
        
def walk(cave,invisited,twoferUsed):
    global pathCount
    visited = invisited.copy()
    print(f"Walking {cave} - been to {visited}")
    visited.append(cave.name)
    if cave.name == 'end':
        print(f"Reached End {visited}")
        pathCount = pathCount + 1
        return visited
    for candidate in cave.adjacents:
        if (not candidate.isLarge) and (candidate.name in visited and not twoferUsed) and (candidate.name not in ["start","end"]):
            print(f"Visiting {candidate} using twofer")
            walk(candidate,visited,True) 
        elif candidate.isLarge or candidate.name not in visited: #
            print(f"Visiting {candidate} twofer: {twoferUsed}")
            walk(candidate,visited,twoferUsed)
    visited.pop()

inputs = ["input.test","input.test2","input.test3","input"]
for filename in inputs:
    # Use a dict - so we don't need to care about dupes.
    caves = {}
    paths = {}
    pathCount = 0
    readNodes(filename)
    walk(caves['start'],[],False)
    print(f"Found {pathCount} Paths in {filename}")