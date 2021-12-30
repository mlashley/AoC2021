#!/usr/bin/python3

def load(filename):
    a = []
    for l in open(filename,"r").readlines():
        a.append(list(l.strip()))
    return a


def stepE(arr):
    global moves # I hate myself ;-)
    acopy = [row[:] for row in arr]
    w=len(arr[0])
    for y,v1 in enumerate(acopy):
        for x,v2 in enumerate(v1):
            if v2 == '>':
                if acopy[y][(x+1) % w] == '.':
                    # print(f"x,y {x},{y} moving")
                    moves += 1
                    arr[y][(x+1) % w] = '>'
                    arr[y][x] = '.'
    return arr

def stepS(arr):
    global moves
    acopy = [row[:] for row in arr]

    h=len(arr)
    for y,v1 in enumerate(acopy):
        for x,v2 in enumerate(v1):
            if v2 == 'v':
                if acopy[(y+1) % h][x] == '.':
                    # print(f"x,y {x},{y} moving")
                    moves += 1
                    arr[(y+1) % h][x] = 'v'
                    arr[y][x] = '.'
    return arr


def step(arr):
    return stepS(stepE(arr))


def dump(arr):
    for r in arr:
        print("".join(r))

moves=0

def tests():
    assert stepE([list('...>>>>>...')]) == [list('...>>>>.>..')]
    assert stepS([list('v.v'),list('..v')]) == [ list('..v'),list('v.v')]
    test2= load("input.test2")
    dump(step(test2))

    test3=load("input.test3")
    for s in range(5):
        print(f"Step {s}")
        dump(test3)
        test3=step(test3)
    dump(test3)

def part1(f):
    global moves
    part1=load(f)
    c=0
    moves=1
    while moves != 0:
        moves=0
        c+=1
        part1=step(part1)
        # print(f"Step{c}")
        # dump(part1)

    print(f"Part 1: {f} stable in {c}")

part1("input.test")
part1("input")