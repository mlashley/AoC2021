#!/usr/bin/python3 
import math

f = open("input","r")
# f = open("input.test","r")

horiz = 0
depth = 0

for line in f.readlines():
    (dir,t) = line.split(' ')
    cnt=int(t)
    if dir == "forward":
        horiz = horiz + cnt
    elif dir == "down":
        depth = depth + cnt
    elif dir == "up":
        depth = depth - cnt
    
    print("{} {} to {} {}".format(dir,cnt,horiz,depth))

print("The answer is ", horiz*depth)


