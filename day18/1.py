#!/usr/bin/python3 
import re

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
        print(f"Explode {n[0]},{n[1]}")
        # Replace pair with zero
        return n[0],n[1],True

    if type(n[0]) == int:
        lval = n[0]
    if type(n[1]) == int:
        rval = n[1]

    if type(n[0]) == list:
        newl,newr,zapme = deep(n[0],depth+1,lval,rval)

        if zapme:
            n[0] = f"MARKER_{newl}_{newr}_MARKER"
            zapme = False

        print(f"return from left {newl} {newr} {zapme}")
        return newl,newr,zapme

    if type(n[1]) == list:
        newl,newr,zapme = deep(n[1],depth+1,lval,rval)

        if zapme:
            n[1] = f"MARKER_{newl}_{newr}_MARKER"
            zapme = False

        # Done
        print(f"return from right {newl} {newr} {zapme}")
        return newl,newr,zapme

    print(f"return from end d{depth}")
    return None,None,False # lval, rval, zapme

def explodeNum(n):
    qq=n.copy()
    print(f"Before: {qq}")
    deep(qq,0,None,None)
    print(f"After: {qq}")
    s = str(qq)
    m = re.search("(.*)'MARKER_(\d)_(\d)_MARKER'(.*)",s)
    if m:
        pre  = m.group(1)
        addl = int(m.group(2))
        addr = int(m.group(3))
        post  = m.group(4)
        print("Before: PRE:",pre,"Nums:",addl,addr,"POST:",post)

        # Add addl to last number in pre (if any)
        m = re.search(r".*(\d+)", pre)
        if m:
            st = m.span(1)[0]
            ed = m.span(1)[1]
            replace = int(pre[st:ed]) + addl
            pre = pre[:st] + str(replace) + pre[ed:]

        # add addr to first number in post (if any)
        m = re.search(r"(\d+)", post)
        if m:
            st = m.span(1)[0]
            ed = m.span(1)[1]
            replace = int(post[st:ed]) + addr
            post = post[:st] + str(replace) + post[ed:]
    
        print("After: PRE:",pre,"Nums:",addl,addr,"POST:",post)

        # Replace exploder with Zero
        s= pre + "0" + post
    print("End Explode:",s)
    return eval(s)
    


# deep([[[[[9,8],1],2],3],4],depth=0,lval=0,rval=0)

    
assert explodeNum([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
print("-----------------")
assert explodeNum([[[[[9,8],1],2],3],4]) == [[[[0,9],2],3],4]
print("-----------------")
assert explodeNum([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]
print("-----------------")
assert explodeNum([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
print("-----------------")
assert explodeNum([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[7,0]]]]


for line in f.readlines():
    snailNum = eval(line.strip()) # Security - Possible lack of input sanitization ;-)
    assert len(snailNum) == 2
    assert depth(snailNum) <= 4



