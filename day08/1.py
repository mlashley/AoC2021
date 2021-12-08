#!/usr/bin/python3 

f = open("input","r")
# f = open("input.test","r")

def is1478(x):
    l = len(x)
    return (l == 7) or (l>=2 and l<=4)

c=0
for line in f.readlines():
    x = line.split('|')
    for digit in x[1].split():
        c=c+is1478(digit)

print(f"Count = {c}")