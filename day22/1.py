#!/usr/bin/python3
import re
import numpy as np

worldmin=-50
worldmax=50

# world to 0-based array, trnacates and returns noneType for outside the world.
def a(w):
    if w>= worldmin and w <= worldmax:
        return w+abs(worldmin)

# 0-based array to world (unused)
def W(a):
    w=a-abs(worldmin)
    if w>= worldmin and w <= worldmax:
        return w
    else:
        raise ValueError(f"Invalid array offset {a} for world {worldmin}..{worldmax}")

assert a(-50)==0
assert a(50)==100

# Part1

def part1(filename):

    world = np.zeros((101,101,101),dtype=np.byte)
    with open(filename,"r") as f:
        worldmin=0
        worldmax=0
        for line in f:
            # on x=-48..-1,y=-5..47,z=-40..7
            m = re.match(r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)",line)
            on = m.group(1) == 'on'

            worldmin = min(worldmin, min([int(i) for i in m.groups()[1:]]))
            worldmax = max(worldmax, max([int(i) for i in m.groups()[1:]]))
            xmin,xmax,ymin,ymax,zmin,zmax=[a(int(x)) for x in m.groups()[1:]]
            
            if not None in [xmin,xmax,ymin,ymax,zmin,zmax]: # Could be out of range in only 1 dimension, check all.
                if on:
                    world[xmin:xmax+1,ymin:ymax+1,zmin:zmax+1] = np.ones((1+xmax-xmin,1+ymax-ymin,1+zmax-zmin))
                else:
                    world[xmin:xmax+1,ymin:ymax+1,zmin:zmax+1] = np.zeros((1+xmax-xmin,1+ymax-ymin,1+zmax-zmin))


    ans = np.sum(world)
    print(f"{filename} answer {ans} [ WorldMin/Max {worldmin} / {worldmax}") # We know that the size of the world wil bite us in the ass in Part2...
    return ans

assert part1("input.test1") == 39
assert part1("input.test") == 590784
part1("input")