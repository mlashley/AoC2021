#!/usr/bin/python3 

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
    # Build the expanded pair of pairs e.g. AC -> B input goes to k: AC v: [AB,BC]
    pairDict[x[0]] =  [ x[0][0]+x[1], x[1]+x[0][1] ]

def polymerize(d):
    newDict = {} 
    newPairs = []
    for pair in d.keys():
        # print(f"{pair} => {pairDict[pair]}")
        for newpair in pairDict[pair]:
            if newpair in newDict.keys():
                newDict[newpair] += d[pair]
            else:
                # print(f"New = {newpair}")
                newDict[newpair] = d[pair]
    return newDict

def statsDumpTemplate(d,lastChar):
    countDict={}
    for k in d.keys():
        char = k[0]
        val = d[k]
        if char in countDict.keys():
            countDict[char] += val
        else: 
            countDict[char] = val
    countDict[lastChar] += 1
    # print(countDict)
    s = [ v for k, v in sorted(countDict.items(), key=lambda item: item[1]) ]
    minC=s[0]
    maxC=s[-1]
    length = sum([ countDict[k] for k in countDict.keys() ])
    return f"max {maxC} - min {minC} = {maxC-minC}\t[len {length}]"

pairs = [ "".join(p) for p in zip(template[::1], template[1::1])]

d={}
# Unnecessary conditional since _our_ initial template is all unique pairs
for p in pairs:
    if p in d.keys():
        d[p] += 1
    else:
        d[p] = 1

lastChar = template[-1]
for i in range(40):
    d = polymerize(d)
    print(f"Iter: {i+1}",statsDumpTemplate(d,lastChar))