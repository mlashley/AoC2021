#!/usr/bin/python3 
import math

f = open("input.1","r")
# f = open("testinput","r")

last=float("nan")
increased = 0

data = f.readlines()

print("Read {} line iterating from 0 to {}".format(len(data),len(data)-3))

for idx in range(0,len(data)-3):
    A = float(data[idx])   + float(data[idx+1]) + float(data[idx+2])
    B = float(data[idx+1]) + float(data[idx+2]) + float(data[idx+3])
    
    if B > A:
        # print(idx,"increased",A,B)
        increased = increased + 1
    else:
        # print(idx,"not",A,B)

print("{} Increased".format(increased))


