#!/usr/bin/python3 
import re

def addNum(a,b):
    return[a,b]

def splitToPair(n):
    left = n//2
    right = -(-n//2)
    return [left,right]

def maxDepth(n):
    l = 0
    r = 0
    if type(n[0]) == list:
        l = maxDepth(n[0])
    if type(n[1]) == list:
        r = maxDepth(n[1])
    return 1+max(l,r)

def maxNum(n):
    if type(n[0]) == list:
        l = maxNum(n[0])
    else:
        l = n[0]
    if type(n[1]) == list:
        r = maxNum(n[1])
    else:
        r = n[1]
    return max(l,r)

# zapme=True => nuke parent, zapme=False - we already did. Zapme=None - TODO.
def deep(n,depth,lval,rval):
    # print(f"deep d:{depth} {n} lval:{lval} rval:{rval}")
    zapme = None
    
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

        if zapme == True:
            n[0] = f"MARKER_{newl}_{newr}_MARKER"
            zapme = False

        if zapme != None:
            # print(f"return from left {newl} {newr} {zapme}")
            return newl,newr,zapme

    if type(n[1]) == list:
        newl,newr,zapme = deep(n[1],depth+1,lval,rval)

        if zapme == True:
            n[1] = f"MARKER_{newl}_{newr}_MARKER"
            zapme = False

        if zapme != None:
            # print(f"return from right {newl} {newr} {zapme}")
            return newl,newr,zapme

    # print(f"return from end d{depth}")
    return None,None,zapme # lval, rval, zapme

def explodeNum(n):
    qq=n.copy()
    print(f"deep-Before: {qq}")
    deep(qq,0,None,None)
    print(f"deep-After: {qq}")
    s = str(qq)
    m = re.search("(.*)'MARKER_(\d+)_(\d+)_MARKER'(.*)",s)
    if m:
        pre  = m.group(1)
        addl = int(m.group(2))
        addr = int(m.group(3))
        post  = m.group(4)
        print("explodeNum-Before: PRE:",pre,"Nums:",addl,addr,"POST:",post)

        # Add addl to last number in pre (if any)
        # Pay close attention to the fucking regex - don't precede \d+ with a greedy operator and expect it to work for numbers >9
        # NB - I was angry at the amount of time I spent finding this - hence the naive lookback now.
        m = re.search(r".*(\d+)", pre)
        if m:
            st = m.span(1)[0]
            ed = m.span(1)[1]
            while(pre[st-1].isdigit()): # Include preceding digits.
                st += -1
            replace = int(pre[st:ed]) + addl
            pre = pre[:st] + str(replace) + pre[ed:]

        # add addr to first number in post (if any)
        m = re.search(r"(\d+)", post)
        if m:
            st = m.span(1)[0]
            ed = m.span(1)[1]

            replace = int(post[st:ed]) + addr
            post = post[:st] + str(replace) + post[ed:]
    
        print("explodeNum-After: PRE:",pre,"Nums:",addl,addr,"POST:",post)

        # Replace exploder with Zero
        s= pre + "0" + post
    print("End Explode:",s)
    return eval(s)

def splitNum(n):
    s = str(n)
    print(f"splitNum-Before: {s}")
    m = re.search(r"(\d{2,})",s)
    if m:
        st = m.span(1)[0]
        ed = m.span(1)[1]
        replace = splitToPair(int(s[st:ed]))
        s = s[:st] + str(replace) + s[ed:]
    print(f"splitNum-After: {s}")
    return eval(s)

def reduceNum(n):
    while True:
        md = maxDepth(n)
        mn = maxNum(n)
        if md >= 5:
            print(f"reduceNum=maxDepth {md}")
            n=explodeNum(n)
        elif mn >= 10:
            print(f"reduceNum=maxNum {mn} md:{md}")
            n=splitNum(n)
        else:
            print("===========================")
            return n

def magnitude(n):
    if type(n[0]) == int:
        lval = n[0]
    elif type(n[0]) == list:
        lval = magnitude(n[0])

    if type(n[1]) == int:
        rval = n[1]
    elif type(n[1]) == list:
        rval = magnitude(n[1])
    return (3*lval)+(2*rval)

def sumFile(filename):
    f = open(filename,"r")
    first=True
    for line in f.readlines():
        snailNum = eval(line.strip()) # Security - Possible lack of input sanitization ;-)
        assert len(snailNum) == 2
        assert maxDepth(snailNum) <= 4
        if first:
            total = snailNum
            first=False
        else:
            total = reduceNum(addNum(total,snailNum))
    print(f"Total for {filename} is {total}")
    return total

def maxSum(filename):
    maxMagnitude = 0
    f = open(filename,"r")
    lines = f.readlines()
    for l1 in lines:
        for l2 in lines:
            n1 = eval(l1.strip()) # needs to be reset each loop as we clobber...
            if l1 != l2:
                n2 = eval(l2.strip())
                t = magnitude(reduceNum(addNum(n1,n2)))
                if t > maxMagnitude:
                    maxMagnitude = t
                    print(f"New Best {maxMagnitude} from {n2} + {n1}")
    print(f"Max Magnitude for 2 numbers in {filename} is {maxMagnitude}")
    return maxMagnitude

selfTest=False
if selfTest:

    assert addNum([1,2],[[3,4],5]) == [[1,2],[[3,4],5]]

    assert splitToPair(10) == [5,5]
    assert splitToPair(11) == [5,6]

    assert maxDepth([1,[2,[3,4]]]) == 3
    assert maxDepth([[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]) == 4

    assert maxNum([[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]) == 8
    assert maxNum([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == 9

    assert splitNum([7,[6,[15,[4,[3,2]]]]]) == [7,[6,[[7,8],[4,[3,2]]]]]

    assert explodeNum([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
    assert explodeNum([[[[[9,8],1],2],3],4]) == [[[[0,9],2],3],4]
    assert explodeNum([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]
    assert explodeNum([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
    assert explodeNum([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[7,0]]]]

    # This is the simple worked example
    a=[[[[4,3],4],4],[7,[[8,4],9]]]
    b=[1,1]
    assert reduceNum(addNum(a,b)) == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

    assert magnitude([9,1]) == 29
    assert magnitude([1,9]) == 21
    assert magnitude([[9,1],[1,9]]) == 129
    assert magnitude([[1,2],[[3,4],5]]) == 143
    assert magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]]) == 1384
    assert magnitude([[[[1,1],[2,2]],[3,3]],[4,4]]) == 445
    assert magnitude([[[[3,0],[5,3]],[4,4]],[5,5]]) == 791
    assert magnitude([[[[5,0],[7,4]],[5,5]],[6,6]]) == 1137
    assert magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]) == 3488

    # All test input in steps.

    a=[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    b=[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    c=[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
    assert reduceNum(addNum(a,b)) == c
    a=[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
    b=[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    c=[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
    assert reduceNum(addNum(a,b)) == c
    a=[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
    b=[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
    c=[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
    assert reduceNum(addNum(a,b)) == c
    a=[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
    b=[7,[5,[[3,8],[1,4]]]]
    c=[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
    assert reduceNum(addNum(a,b)) == c
    a=[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
    b=[[2,[2,2]],[8,[8,1]]]
    c=[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
    assert reduceNum(addNum(a,b)) == c
    a=[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
    b=[2,9]
    c=[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
    assert reduceNum(addNum(a,b)) == c
    a=[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
    b=[1,[[[9,3],9],[[9,0],[0,7]]]]
    c=[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
    assert reduceNum(addNum(a,b)) == c
    a=[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
    b=[[[5,[7,4]],7],1]
    c=[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
    assert reduceNum(addNum(a,b)) == c

    a=[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
    b=[[[[4,2],2],6],[8,7]]
    c=[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
    assert reduceNum(addNum(a,b)) == c

    assert sumFile("input.test2") == [[[[1,1],[2,2]],[3,3]],[4,4]]
    assert sumFile("input.test3") == [[[[3,0],[5,3]],[4,4]],[5,5]]
    assert sumFile("input.test4") == [[[[5,0],[7,4]],[5,5]],[6,6]]
    assert sumFile("input.test5") == [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
    assert magnitude(sumFile("input.test5")) == 4140

    assert sumFile("input.test") == [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]

    assert reduceNum(addNum([[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]])) == [[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]
    assert magnitude([[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]) == 3993
    assert maxSum("input.test5") == 3993

print("Part1 Answer", magnitude(sumFile("input")))
print("Part2 Answer",maxSum("input"))