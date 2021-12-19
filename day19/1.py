#!/usr/bin/python3
import re
import numpy as np
# from itertools import permutations

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
        m=re.match(r"--- scanner (\d) ---", f.readline().strip())
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

scanners = loadFile("input.test")
# Naive and not actually true for (1,1,-1) or (2,-2,2) etc...
assert len(set(str(r) for r in scanners[0].beacons[0].allRot())) == 24
assert len(set(str(r) for r in scanners[0].beaconsRotations[0])) == 24

def match(scana,scanb):
    i=0
    for brotation in range(24):
        print(f"Testing B-Rotation {brotation} i: {i}")
        for anchora in scana.beaconsRotations:
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

# for i in range(5):

todolist = list(range(1,len(scanners)))
donelist = [ 0 ]

while todolist:
    print("(Re)start while")
    found=False
    for i1 in donelist:
        for i2 in todolist:
            print(f"Checking scanner {i1} vs {i2}.. done {donelist} todo {todolist}")
            rot,offset = match(scanners[i1],scanners[i2])
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

for s in scanners:
    print(s.number,s.myRotation, s.myOffset)

# from s0

# -618,-824,-621
# -537,-823,-458
# -447,-329,318
# 404,-588,-901
# 544,-627,-890

# from s1

# 686,422,578
# 605,423,415
# 515,917,-361
# -336,658,858
# -476,619,847

# --- scanner 0 ---
# 404,-588,-901  <= 4
# 528,-643,409
# -838,591,734
# 390,-675,-793
# -537,-823,-458  <= 2
# -485,-357,347
# -345,-311,381
# -661,-816,-575
# -876,649,763
# -618,-824,-621  <= 1
# 553,345,-567
# 474,580,667
# -447,-329,318  <= 3
# -584,868,-557
# 544,-627,-890  <= 5
# 564,392,-477
# 455,729,728
# -892,524,684
# -689,845,-530
# 423,-701,434
# 7,-33,-71
# 630,319,-379
# 443,580,662
# -789,900,-551
# 459,-707,401

# --- scanner 1 ---
# 686,422,578  <= 1 
# 605,423,415  <= 2
# 515,917,-361 <= 3
# -336,658,858 <= 4
# 95,138,22    <= 5
# -476,619,847
# -340,-569,-846
# 567,-361,727
# -460,603,-452
# 669,-402,600
# 729,430,532
# -500,-761,534
# -322,571,750
# -466,-666,-811
# -429,-592,574
# -355,545,-477
# 703,-491,-529
# -328,-685,520
# 413,935,-424
# -391,539,-444
# 586,-435,557
# -364,-763,-893
# 807,-499,-711
# 755,-354,-619
# 553,889,-390


