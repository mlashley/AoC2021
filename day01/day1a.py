#!/usr/bin/python3 
import math

f = open("input.1","r")

last=float("nan")
increased = 0

for reading in f.readlines():
    if not math.isnan(last):
        if float(reading) > last:
            increased = increased + 1
    last=float(reading)

print("{} Increased".format(increased))


