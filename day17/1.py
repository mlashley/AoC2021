#!/usr/bin/python3

import re

inputs = [  # "target area: x=20..30, y=-10..-5",
            "target area: x=169..206, y=-108..-68"]

class Target:
    def __init__(self,s):
        m=re.match("target area: x=(-?[0-9]+)\.\.(-?[0-9]+), y=(-?[0-9]+)\.\.(-?[0-9]+)",s)
        if m:
            self.xmin=int(m.group(1))
            self.xmax=int(m.group(2))
            self.ymin=int(m.group(3))
            self.ymax=int(m.group(4))
        else:
            raise ValueError("WTF is this? " + s)

    def inTarget(self,probe):
        return self.xmin <= probe.x and probe.x <= self.xmax and self.ymin <= probe.y and probe.y <= self.ymax 
    def __repr__(self):
        return f"Target Acquired {self.xmin},{self.xmax},{self.ymin},{self.ymax}"

class Probe:
    def __init__(self,vx,vy):
        self.x=0
        self.y=0
        self.vx=vx
        self.vy=vy
        self.maxy=0
    def step(self):
        self.x += self.vx
        self.y += self.vy
        if self.vx > 0:
            self.vx += -1
        elif self.vx < 0:
            self.vx += 1
        self.vy += -1
        self.maxy=max(self.y,self.maxy)

    def __repr__(self):
        return f"Probe[@{self.x},{self.y} V:{self.vx},{self.vy}]"

# Yeah so this is totally brute-force and probably will bite me in the ass in part 2...

def tosser(target):
    print(target)
    best = { 'ix': 0, 'iy':0, 'maxy': 0 }
    for ix in range(200):
        for iy in range(200):
            maxy = toss(ix,iy,target)
            if maxy > best['maxy']:
                best = { 'ix': ix, 'iy': iy, 'maxy': maxy}
                print(f"New Best {best}")
    print(f"End Best {best}")            

def toss(ix,iy,target):
    p = Probe(ix,iy)
    hit = False
    while p.vx != 0 or p.y > target.ymin:
        # print(p)
        p.step()
        if target.inTarget(p):
            print(f"Hit {ix},{iy} Max{p.maxy}")
            return p.maxy
    # print(f"Miss {ix},{iy}")
    return -99999   

for input in inputs:
    target = Target(input)
    tosser(target)

