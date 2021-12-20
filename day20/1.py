#!/usr/bin/python3

def load(filename):
    with open(filename,"r") as f:
        algo=f.readline().strip()
        if f.readline() != "\n":
            raise ValueError("Mangled Input")
        img=[]
        for line in f.readlines():
            img.append(line.strip())
        return algo,img

# To apply a 3x3 mask - we need to expand the image by 2px on all sides
# Except these are infinite - so we may need to expand 'more'... ;-)

def expand(img,extra=2):
    y=len(img)
    x=len(img[0])
    
    print(f"Expanding {x} * {y} image")
    startend="."*(x+(2*extra))
    outimg=[]
    for row in range(extra):
        outimg.append(startend)
    for row in img:
        outimg.append(("."*extra)+row+("."*extra))
    for row in range(extra):
        outimg.append(startend)
    return outimg

def reduce(img,extra=2):
    y=len(img)
    x=len(img[0])
    print(f"Reducing {x} * {y} image by {extra} px per side")
    outimg=[]
    for rowNum in range(extra,y-extra):
        outimg.append(img[rowNum][extra:x-extra])
    return outimg

def valAt(x,y,img):
    bits=""
    for ny in range(y-1,y+2):
        bits += img[ny][x-1:x+2]
    bits = bits.replace("#","1")
    bits = bits.replace(".","0")
    return int(bits,2)

def newBitAt(x,y,img,alg):
    return alg[valAt(x,y,img)]

def printImg(img):
    count=0
    for row in img:
        print(row)
        count += sum([int(c) for c in row.replace("#","1").replace(".","0")])
    print(f"Count: {count} [ {len(img)} x {len(img[0])} ]")
    return count

def applyMask(img,alg):
    y=len(img)
    x=len(img[y-1])
    outimg = []
    for rowNum in range(1,y-1):
        newRow=""
        for colNum in range(1,x-1):
            newRow += newBitAt(colNum,rowNum,img,alg)
        outimg.append(newRow)
    return outimg

def unitTests():

    a,i=load("input")
    i=expand(i,2)

    assert len(i) == 104
    assert len(i[0]) == 104
    assert len(i[50]) == 104
    assert len(i[101]) == 104

    assert valAt(2,2,i) == 24
    assert valAt(3,3,i) == 394
    assert valAt(4,3,i) == 348

    i=expand(i,10)
    assert len(i) == 124

    a,i=load("input.test")
        
    assert printImg(i) == 10
    i = expand(i)
    assert printImg(i) == 10
    i=applyMask(i,a)
    assert printImg(i) == 24
    i=applyMask(expand(i),a)
    assert printImg(i) == 35

    for z in range(5):
        i=applyMask(expand(i),a)
        printImg(i)

def malcTests():
    a,i=load("input.test2")
    printImg(i)
    i=expand(i,10)
    printImg(i)
    i=applyMask(i,a)
    printImg(i)
    i=applyMask(i,a)
    printImg(i)

def part1():
    a,i=load("input")
    printImg(i)
    i=applyMask(expand(i,20),a)
    printImg(i)
    i=applyMask(i,a)
    printImg(i)
    i=reduce(i,3)
    printImg(i)


def part2():
    iters=50
    a,i=load("input")
    printImg(i)
    i=expand(i,150)
    for c in range(iters):
        i=applyMask(i,a)
    printImg(i)
    
# unitTests()
# malcTests()
part1()
part2()