#!/usr/bin/python3 

f = open("input","r")
f = open("input.test","r")


def add(a,b):
    return[a,b]

assert add([1,2],[[3,4],5]) == [[1,2],[[3,4],5]]

def splitNum(n):
    left = n//2
    right = -(-n//2)
    return (left,right)

assert splitNum(10) == (5,5)
assert splitNum(11) == (5,6)

def depth(n):
    l = 0
    r = 0
    if type(n[0]) == list:
        l = depth(n[0])
    if type(n[1]) == list:
        r = depth(n[1])
    return 1+max(l,r)

assert depth([1,[2,[3,4]]]) == 3
assert depth([[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]) == 4

def deep(n,depth,lval,rval):
    print(f"deep d:{depth} {n} lval:{lval} rval:{rval}")
    
    if depth == 4:
        newr=None
        newl=None 
        if lval != None:
            newl = lval+n[0]

        if rval != None:
            newr = rval+n[1]
        
        print(f"new {newl},{newr}  from {lval}+{n[0]} and {rval}+{n[1]}")
        # Replace pair with zero
        return newl,newr,True

    if type(n[0]) == int:
        lval = n[0]
    if type(n[1]) == int:
        rval = n[1]

    if type(n[0]) == list:
        newl,newr,zapme = deep(n[0],depth+1,lval,rval)

        if zapme:
            n[0] = 0
            zapme = False

        if newr != None:
            if type(n[1]) == int:
                    print(f"R1-Replace {n[1]} with {newr}")
                    n[1] = newr
                    newr=None # stop filter-up
            
        if newl != None:
            if type(n[0]) == int:
                    print(f"L1-Replace {n[0]} with {newl}")
                    n[1] = newl
                    newl=None # stop filter-up

        # Done
        print(f"return from left {newl} {newr} {zapme}")
        return newl,newr,zapme

    if type(n[1]) == list:
        newl,newr,zapme = deep(n[1],depth+1,lval,rval)

        if zapme:
            n[1] = 0
            zapme = False

        if newl != None:
            if type(n[0]) == int:
                    print(f"L2-Replace {n[0]} with {newl}")
                    n[0] = newl
                    newl=None # stop filter-up
            
        if newl != None:
            if type(n[0]) == int:
                    print(f"L2-Replace {n[0]} with {newl}")
                    n[1] = newl
                    newl=None # stop filter-up
        # Done
        print(f"return from right {newl} {newr} {zapme}")
        return newl,newr,zapme

    print(f"return from end  {newl} {newr} {zapme}")
    return None,None,False # lval, rval, zapme

def explodeNum(n):
    qq=n.copy()
    print(f"Before: {qq}")
    deep(qq,0,None,None)
    print(f"After: {qq}")
    return qq
    


# deep([[[[[9,8],1],2],3],4],depth=0,lval=0,rval=0)

    

assert explodeNum([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]

assert explodeNum([[[[[9,8],1],2],3],4]) == [[[[0,9],2],3],4]
assert explodeNum([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
assert explodeNum([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]

assert explodeNum([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[7,0]]]]


for line in f.readlines():
    snailNum = eval(line.strip()) # Security - Possible lack of input sanitization ;-)
    assert len(snailNum) == 2
    assert depth(snailNum) <= 4



