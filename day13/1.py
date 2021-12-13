#!/usr/bin/python3 
import numpy as np

f = open("input","r")
# f = open("input.test","r")

x=[]
y=[]
points=[]
folds=[]
brk = True
for line in f.readlines():
    if line == "\n":
        brk=False
        continue
    if brk:
        point = line.strip().split(',')
        points.append(tuple([int(p) for p in point]))
        x.append(int(point[0]))
        y.append(int(point[1]))
    else:
        folds.append(line.strip().split(' ')[2].split('='))
    

WIDTH = max(x)+1
HEIGHT = max(y)+1
# print(x,y,WIDTH,HEIGHT,folds) #,points)

arr = np.full((WIDTH,HEIGHT),0)
for p in points:
    arr[p[0],p[1]] = 1

def foldy(arr):
    xmax = arr.shape[1]
    ymax = arr.shape[0]
    half = int((xmax-1)/2)
    for y in range(ymax):
        for x in range(half):
            refl_x = (xmax-1)-x
            arr[y,x] = arr[y,x] + arr[y,refl_x]
    return arr[:,0:half]

def foldx(arr):
    xmax = arr.shape[1]
    ymax = arr.shape[0]
    half = int((ymax-1)/2)
    for x in range(xmax):
        for y in range(half):
            refl_y = (ymax-1)-y
            arr[y,x] = arr[y,x] + arr[refl_y,x]
    return arr[0:half,:]

def dump(arr,verbose):
    count=0
    outstr=""
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            out="."
            if arr[y,x] > 0:
                # print(arr[y,x],end="")
                out="#"
                count +=1
            outstr += out 
        outstr += "\n"
    if(verbose):
        print(outstr)
    print(f"== Count:{count} ====")
    

print("First fold count follows:")

for fold in folds:   
    if fold[0] == 'y':
        arr = foldy(arr)
    elif fold[0] == 'x':
        arr = foldx(arr)        
    else:
        raise ValueError("WTF?")
    dump(arr,False)

dump(arr,True)