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


def floodFill(x,y,arr,shadow):

    shadow[y][x]="+"
    if(x > 0):
        nx=x-1
        ny=y
        if (arr[ny][nx] < 9) and shadow[ny][nx]!="+":
            shadow[ny][nx]="+"
            floodFill(nx,ny,arr,shadow)
    if(y > 0):
        nx=x
        ny=y-1
        if (arr[ny][nx] < 9) and shadow[ny][nx]!="+":
            shadow[ny][nx]="+"
            floodFill(nx,ny,arr,shadow)
    if(x+1 < len(arr[0])):
        nx=x+1
        ny=y
        if (arr[ny][nx] < 9) and shadow[ny][nx]!="+":
            shadow[ny][nx]="+"
            floodFill(nx,ny,arr,shadow)

    if(y+1 < len(arr)):
        nx=x
        ny=y+1
        if (arr[ny][nx] < 9) and shadow[ny][nx]!="+":
            shadow[ny][nx]="+"
            floodFill(nx,ny,arr,shadow)


sum=0
basins=[]
for y in range(len(arr)):
    for x in range(len(arr[0])):
        if isLowest(x,y,arr):
            sum=sum+arr[y][x]+1
            print("{} at {},{} is lowest".format(arr[y][x],x,y,isLowest))
            shadow=[["." for q in arr[0]] for row in arr]
            floodFill(x,y,arr,shadow)
            shadowcount=0
            for row in shadow:
                print("".join(row))
                shadowcount=shadowcount+len("".join(row).replace(".",""))
            print(f"Basin Size {shadowcount}")
            basins.append(shadowcount)

print(f"Sum = {sum}")
basins.sort()
print("3 large basins ",basins[-1]*basins[-2]*basins[-3])
    
                
                

