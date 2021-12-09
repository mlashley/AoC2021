#!/usr/bin/python3 

f = open("input","r")
# f = open("input.test","r")

arr=[]
for line in f.readlines():
    arr.append([int(x) for x in line.strip()])


def getAdjacent(x,y,arr):
    out=[]
    if(x > 0):
        out.append(arr[y][x-1])
    if(y > 0):
        out.append(arr[y-1][x])
    if(x+1 < len(arr[0])):
        out.append(arr[y][x+1])
    if(y+1 < len(arr)):
        out.append(arr[y+1][x])
    # print("Adjacent to {} {} is {}".format(x,y,out))
    return out

def isLowest(x,y,arr):   
    isLowest=True
    for p in getAdjacent(x,y,arr):
        if p <= arr[y][x]:
            isLowest=False
    return isLowest


sum=0
for y in range(len(arr)):
    for x in range(len(arr[0])):
        if isLowest(x,y,arr):
            sum=sum+arr[y][x]+1
            print("{} at {},{} is lowest".format(arr[y][x],x,y,isLowest))

print(f"Sum = {sum}")