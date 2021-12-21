#!/usr/bin/python3
from functools import cache, reduce

# input:
# Player 1 starting position: 7
# Player 2 starting position: 4

class Die:
    def __init__ (self,sides,startingvalue=1):
        self.sides=sides
        self.next = startingvalue
        self.rollCount = 0
    def roll(self,count=1):
        # Perform N rolls, return sum
        rolls = [ self.nextval() for x in range(count)]
        # print(f"Rolled {rolls}")
        self.rollCount += count
        return sum(rolls)
    def nextval(self):
        r=self.next
        self.next += 1
        if self.next > self.sides: # Too lazy to figure out % math.
            self.next = 1
        return r

class Player:
    def __init__ (self,startpos):
        self.pos = startpos
        self.score = 0
    def getPos(self):
        return self.pos
    def move(self,d):
        self.pos += d.roll(3)
        self.pos -=  ((self.pos-1)//10)*10 # Wrap, 1-based.
        self.score += self.getPos()

    def __str__(self):
        return f"Player[p:{self.pos} s:{self.score}]"
    def __repl__(self):
        return self.__str()

def unitTests():

    d = Die(10)
    assert [ d.roll(),d.roll(),d.roll(),d.roll()] == [1,2,3,4]
    assert d.roll(4) == 26
    assert d.roll(3) == 20

    d = Die(100)
    p1 = Player(4)
    p2 = Player(8)
    print(p1)
    while True:
        p1.move(d)
        print("1",p1)
        if p1.score >= 1000:
            assert p2.score * d.rollCount == 739785
            break
        p2.move(d)
        print("2",p2)
        if p2.score >= 1000:
            assert p2.score ==0 # Patently false we expect p2 to win
            break

def part1():
    d = Die(100)
    p1 = Player(7) # <== our input - not reading 2 numbers from file...
    p2 = Player(4)
    while True:
        p1.move(d)
        # print("1",p1)
        if p1.score >= 1000:
            print(f"Player 1 Wins, Part1 answer is {p2.score * d.rollCount}")
            break
        p2.move(d)
        # print("2",p2)
        if p2.score >= 1000:
            print(f"Player 2 Wins, Part1 answer is {p1.score * d.rollCount}")
            break

# Fuck all that OO shit ;-) 
# There are going to be way less than 10*10*21*21 possible _winning_ states of (p1pos,p2pos,p1score,p2score)
# We can _just_ calculate those.

# NB the commented-prints here will run 100K+ times...

dicemap = {3: 1, 9: 1, 4: 3, 8: 3, 5: 6, 7: 6, 6: 7} # score of 3 rolls of d3, combinations

def playerstate(p,s): # Get tuple of pos,score
    return (s[1], s[3]) if p else (s[0], s[2])

def newstate(p, st, npos, nscore):
    if p:
        return (st[0], npos, st[2], nscore)
    else:
        return (npos, st[1], nscore, st[3])

def addt(a,b): # add tuple
    # print(f"Add: {a},{b}")
    return (a[0]+b[0], a[1]+b[1])

def mult(a,x):
    # print(f"Mult: {a},{x}")
    return (a[0]*x, a[1]*x)

def looppos(p) -> int:
    return p-(((p-1)//10)*10)

@cache # This is the magic annotation - we lookup old result once calculated.
def part2(player,st):
    if playerstate(player, st)[1] >= 21: # Did someone win?
        # print("WIN",player,st)
        return (0, 1) if player else (1, 0)
    
    # print("OTHER",player,st)

    player ^= 1 
    pos, score = playerstate(player, st)

    # For each universe fork the 7 possible results for 3 times d3 roll.
    return reduce(
        addt,   (
                    mult( # wincount * probability map for that score (dicemap)
                        part2(player, 
                            newstate(player, st, looppos(pos + k), score + looppos(pos + k)))
                        , dicemap[k]
                    ) for k in dicemap
                )
    )

# unitTests()
part1()
print("Part2 answer",max(part2(1,(7,4,0,0))))
