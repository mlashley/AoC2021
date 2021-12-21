#!/usr/bin/python3

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
        self.zeropos = startpos-1  # store zero-based
        self.score = 0
    def getPos(self):
        return self.zeropos+1 
    def move(self,d):
        self.zeropos = (self.zeropos+d.roll(3)) % 10
        self.score += self.getPos()

    def __str__(self):
        return f"Player[p:{self.zeropos+1} s:{self.score}]"
    def __repl__(self):
        return self.__str()

def unitTests():

    d = Die(10)
    assert [ d.roll(),d.roll(),d.roll(),d.roll(),] == [1,2,3,4]
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
        print("1",p1)
        if p1.score >= 1000:
            print(f"Player 1 Wins, answer is {p2.score * d.rollCount}")
            break
        p2.move(d)
        print("2",p2)
        if p2.score >= 1000:
            print(f"Player 2 Wins, answer is {p1.score * d.rollCount}")
            break

unitTests()
part1()