#!/usr/bin/python3 
import math

f = open("input","r")
# f = open("input.test","r")

horiz = 0
depth = 0
aim = 0

for line in f.readlines():
    (dir,t) = line.split(' ')
    cnt=int(t)
    if dir == "forward":
        horiz = horiz + cnt
        depth = depth + (aim * cnt)
    elif dir == "down":
        aim = aim + cnt
    elif dir == "up":
        aim = aim - cnt
    
    print("{} {} to {} {}".format(dir,cnt,horiz,depth))

print("The answer is ", horiz*depth)


