#!/usr/bin/python3
import re
import numpy as np
from multiprocessing import Pool
from itertools import repeat

ROTATIONS=[]
def init_rot24():
    x=np.zeros((3,3))
    # Build the possible matrices, each column has a single 1 or -1, each row has a a single 1 or -1
    # This gives 48 of which 24 are unique - take the determinant=1 half.
    # c1,c2 values order is crafted to make the no-rotation be the first entry... [ [ 1,0,0 ], [ 0,1,0], [0,0,1] ]
    for c1 in [[1,0,0], [-1,0,0], [0,-1,0], [0,1,0], [0,0,-1],[0,0,1]]:
        x[:,0] = c1
        for c2 in [(1,0),(0,1),(0,-1),(-1,0)]:
            c2idx=0
            for r in range(3):
                if x[r,0] == 0:
                    x[r,1] = c2[c2idx]
                    c2idx += 1
                else:
                    x[r,1] = 0
            for c3 in [1,-1]:
                for r in range(3):
                    if x[r,0]==0 and x[r,1]==0:
                        x[r,2] = c3
                    else:
                        x[r,2] = 0
                if np.linalg.det(x) == 1:
                    ROTATIONS.append(x.copy())
                    
init_rot24()
assert len(set(str(r) for r in ROTATIONS)) == 24

class Scanner:
    def __init__(self,n):
        self.number = n
        self.beacons = []
        self.beaconsRotations = []
        self.myRotation=0
        self.myOffset=[]
    def addBeacon(self,x,y,z):
        self.beacons.append(Beacon(x,y,z))
    def load(self,f):
        m=re.match(r"--- scanner (\d+) ---", f.readline().strip())
        if m:
            self.number=m.group(1)
        else:
            raise ValueError("Did not find Scanner header line")
        for l in f:
            if l == "\n":
                return True # More to come
            elif l == "":
                return None # EOF
            x,y,z = l.strip().split(',')
            self.addBeacon(int(x),int(y),int(z))
    def allRot(self):
        for beacon in self.beacons:
            self.beaconsRotations.append(list(beacon.allRot()))
    def __str__(self):
        return f"Scanner #{self.number} {self.beacons}"
    def __repr__(self):
        return self.__str__()

class Beacon:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def asColumn(self):
        return np.array([self.x,self.y,self.z]).reshape((3,1))
    def allRot(self):
        point = self.asColumn()
        return [ np.matmul(r,point) for r in ROTATIONS ]
    def __str__(self):
        return f"[{self.x},{self.y},{self.z}]"
    def __repr__(self):
        return self.__str__()
    
def loadFile(filename):
    scanners=[]
    f = open(filename,"r")
    more=True
    while more:
        s = Scanner(-1)
        scanners.append(s)
        more=s.load(f)
        s.allRot()
    return scanners

scanners = loadFile("input")
# scanners = loadFile("input.test")
# Naive test, and not actually true for (1,1,-1) or (2,-2,2) etc... but good enough.
assert len(set(str(r) for r in scanners[0].beacons[0].allRot())) == 24
assert len(set(str(r) for r in scanners[0].beaconsRotations[0])) == 24

def match(scana,scanb):
    i=0
    for brotation in range(24):
        # print(f"Testing B-Rotation {brotation} i: {i}")
        for anchora in scana.beaconsRotations[0:15]:   # Shortcut - there are 26 of these - and we need a 12 hit, so check at most 14
            matchCount=0
            for beacona in scana.beaconsRotations:
                if not np.array_equal(anchora[0],beacona[0]):
                    offseta = anchora[0]-beacona[0]  # 0 for fixing a-rotation
                    for anchorb in scanb.beaconsRotations:
                        for beaconb in scanb.beaconsRotations:
                            if not np.array_equal(anchorb[0],beaconb[0]):
                                offsetb = anchorb[brotation]-beaconb[brotation]
                                i += 1
                                if np.array_equal(offseta,offsetb):
                                    matchCount += 1
                                    # print(f"Match++ {matchCount}")
                                    if matchCount >= 11: # because the anchor must match for 12 total
                                        print(f"Shaweeet - Rotation {brotation} Offset {offseta.reshape(1,3)} Pair {anchora[0].reshape(1,3)} {anchorb[brotation].reshape(1,3)} and {beacona[0].reshape(1,3)} {beaconb[brotation].reshape(1,3)}")
                                        x=anchora[0]-anchorb[brotation]
                                        print(f"ScannerOffset {x.reshape(1,3)}")
                                        return brotation,x
    return None,None

# ^^ unused - Parallel version of above below.

def mpmatch(scana,scanb):
    with Pool(24) as pool:
        res = pool.starmap(mpmatch_inside,zip(range(24),repeat(scana),repeat(scanb)))
        print(res)
    for r in res:
        if r !=None:
            return r
    return None,None

def mpmatch_inside(brotation,scana,scanb):
    # print(f"Testing B-Rotation {brotation} i: {i}")
    for anchora in scana.beaconsRotations[0:15]:   # Shortcut - there are 26 of these - and we need a 12 hit, so check at most 14
        matchCount=0
        for beacona in scana.beaconsRotations:
            if not np.array_equal(anchora[0],beacona[0]):
                offseta = anchora[0]-beacona[0]  # 0 for fixing a-rotation
                for anchorb in scanb.beaconsRotations:
                    for beaconb in scanb.beaconsRotations:
                        if not np.array_equal(anchorb[0],beaconb[0]):
                            offsetb = anchorb[brotation]-beaconb[brotation]

                            if np.array_equal(offseta,offsetb):
                                matchCount += 1
                                # print(f"Match++ {matchCount}")
                                if matchCount >= 11: # because the anchor must match for 12 total
                                    print(f"Shaweeet - Rotation {brotation} Offset {offseta.reshape(1,3)} Pair {anchora[0].reshape(1,3)} {anchorb[brotation].reshape(1,3)} and {beacona[0].reshape(1,3)} {beaconb[brotation].reshape(1,3)}")
                                    x=anchora[0]-anchorb[brotation]
                                    print(f"ScannerOffset {x.reshape(1,3)}")
                                    return brotation,x

todolist = list(range(1,len(scanners)))
donelist = [ 0 ]
checked=[]

while todolist:
    print("(Re)start while")
    found=False
    for i1 in donelist:
        for i2 in todolist:
            if f"{i1}_{i2}" in checked:
                print(f"Already done {i1} vs {i2} - skip")
            else:
                print(f"Checking scanner {i1} vs {i2}.. done {donelist} todo {todolist}")
                rot,offset = mpmatch(scanners[i1],scanners[i2])
                checked.append(f"{i1}_{i2}")
                if rot != None:
                    found=True
                    print(f"Scanner{i1}=>{i2} rot:{rot} offset:{offset.reshape((1,3))}")
                    scanners[i2].myRotation = rot
                    scanners[i2].myOffset   = offset
                    # TODO Put rotated+offset value in scanners[i2].beaconsRotations[:][0] for future matching
                    for b in range(len(scanners[i2].beaconsRotations)):
                        scanners[i2].beaconsRotations[b][0] = scanners[i2].beaconsRotations[b][rot] + offset
                    donelist.append(i2)
                    todolist.remove(i2)
                    break
        else:
            continue
        break
    if not found:
        assert ValueError("Motherfucker")

finalbeacons = []
for s in scanners:
    for b in s.beaconsRotations:      
        finalbeacons.append(str(b[0].reshape(1,3)))

print(set(finalbeacons))
print(len(set(finalbeacons))) # Part1 Answer