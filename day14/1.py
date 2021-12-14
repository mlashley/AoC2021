#!/usr/bin/python3 
import numpy as np

f = open("input","r")
# f = open("input.test","r")

pairInsertions=[]
beforeBreak = True
for line in f.readlines():
    if line == "\n":
        beforeBreak=False
        continue
    if beforeBreak:
        template = line.strip()
    else:
        pairInsertions.append([ line.strip().split(' ')[x] for x in [0,2]])

# TODO build this dict as we go above.
pairDict = {}
for x in pairInsertions:
    # Build the expanded string - but leave the last char off
    # e.g. AC -> B goes to AB not ABC.
    # We'll take care of that as it is always the first
    # char of the next pair.
    pairDict[x[0]] = x[0][0]+x[1]

def polymerize(t):
    # For "ABCD" produce the list of overlapping pairs
    # [('A', 'B'), ('B', 'C'), ('C', 'D')]
    pairs = [ "".join(p) for p in zip(t[::1], t[1::1])]
    out=""
    for pair in pairs:
        out=out+pairDict[pair]
    # Special case last char
    out += pairs[-1][1]
    return out

def statsDumpTemplate(t):
    out=""
    maxC=0
    minC=999999
    for c in uniqueChars:
        count = t.count(c)
        if count>maxC:
            maxC=count
        if count<minC:
            minC=count
    out += f"max {maxC} - min {minC} = {maxC-minC}\t[len {str(len(t))}]"
    return out

# Calc once make global
uniqueChars = set(template)
for i in range(10):
    template = polymerize(template)
    print(f"Iter: {i+1}",statsDumpTemplate(template))

