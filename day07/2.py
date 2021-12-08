#!/usr/bin/python3 

f = open("input","r")
# f = open("input.test","r")

crabx = [ int(x) for x in f.readline().strip().split(',') ]
crabx.sort()

bestscore=float('inf')
bestoffset=-1
for x1 in range(crabx[0],crabx[-1]+1):
    # Sum of Natural numbers S = [n(n+1)]/2 
        
    cur = sum([(abs(x1-x2)*(abs(x1-x2)+1))/2 for x2 in crabx])
    if cur < bestscore:
        bestscore=cur
        bestoffset=x1
    # print("Offset {} Sum {}".format(x1,cur))

print(f"Best Offset {bestoffset} Scores {bestscore}")



