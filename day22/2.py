#!/usr/bin/python3
import re
from functools import cache

# Part2

# Start with empty list of cubes.
# For each input action - perform intersect with existing list and add to the list.
# e.g with 2d 
# on 10..12,10..12 - is added to list with onoff=1... (count of on is 3x3=9)
# on 11..13,11..13 - is added to list with onoff=1 _and_ the overlap (11..12,11..12) is added with onoff=-1 to account.
#    count of on is (3x3) + (-(2x2)) + (3x3)

# If c1x1,c2x2 overlaps c2x1,c2x2 then the overlap-range is from the middle pair of points in the sorted list.
def middle(q,w,e,r):
    return sorted((q,w,e,r))[1:3]

# I actually cannot explain why this has a speedup - but we go from 20s to 8s on the main input file... maybe it caches the lambdas?
@cache
def addOverlap(cb1x1,cb1x2,cb1y1,cb1y2,cb1z1,cb1z2,state,cb2x1,cb2x2,cb2y1,cb2y2,cb2z1,cb2z2):   
    getOverlap = lambda: [(*middle(cb2x1,cb1x1,cb2x2,cb1x2),*middle(cb2y1,cb1y1,cb2y2,cb1y2),*middle(cb2z1,cb1z1,cb2z2,cb1z2),-state)] # State is 1,-1 == on/off
    doesNotOverlap = lambda: any(a>b for a,b in zip((cb2x1,cb1x1,cb2y1,cb1y1,cb2z1,cb1z1),(cb1x2,cb2x2,cb1y2,cb2y2,cb1z2,cb2z2)))
    return ( [] if doesNotOverlap() else getOverlap() )

def size(c):
    return ((1+c[1]-c[0])*(1+c[3]-c[2])*(1+c[5]-c[4])) * c[6]

def part2(filename):
    with open(filename,"r") as f:

        cubes = []
        for line in f:
            m = re.match(r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)",line)
            cmd=m.group(1)
            commandCube=[int(i) for i in m.groups()[1:]]
            # print(cmd,commandCube)
            for cube in cubes[:]: # Must iterate over a copy - because we are going to modify it...
                cubes += addOverlap(*cube, *commandCube)
            if cmd == 'on':
                cubes += [(*commandCube,1)]
            # print(cubes)
        
        worldsum=0
        for cube in cubes:
            # print(cube)
            worldsum+=size(cube)
        print(f"For file:{filename} part2 ans {worldsum}")
        return worldsum

assert part2("input.test2") == 2758514936282235
part2("input")