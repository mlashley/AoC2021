#!/usr/bin/python3 

from itertools import permutations

f = open("input","r")
# f = open("input.test","r")

segdigits = [
   "1110111", # 0
   "0010010", # 1
   "1011101", # 2
   "1011011", # 3
   "0111010", # 4
   "1101011", # 5
   "1101111", # 6
   "1010010", # 7
   "1111111", # 8
   "1111011"  # 9
]

def mapper(input,map): # 'be','efgabcd' => 1000100
    out=["0"]* 7
    for c1 in input:
        out[map.index(c1)] = "1"
    return "".join(out)

#print("Test ba gfdeacb is ",mapper("ba","gfdeacb"))

def apply(digits,map):
    soln = ""
    for digit in digits:
        i = mapper(digit,map)
        soln = soln + str(segdigits.index(i))
    return int(soln)
    
# This is only 5K - we could be smarter... but..
perms = [''.join(p) for p in permutations('abcdefg')]

def validate(signals,digits):
    for perm in perms:
        good = True
        for signal in signals:
            if mapper(signal,perm) not in segdigits:
                good = False
                break
        if(good):
            soln = apply(digits,perm)
            print(f"Signals {signals} maps with {perm} for solution {soln}")
            return(soln)

c=0
for line in f.readlines():
    x = line.split('|')
    signals = [ "".join(sorted(y)) for y in x[0].split() ]
    digits  = [ "".join(sorted(y)) for y in x[1].split() ]
    c=c+validate(signals,digits)

print(f"Sum = {c}")



