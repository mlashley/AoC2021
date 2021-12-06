#!/usr/bin/python3 

f = open("input","r")
# f = open("input.test","r")

initial = [ int(x) for x in f.readline().strip().split(',') ]

def doday(school):
    extras = []
    for idx,fishAge in enumerate(school):
        if fishAge > 0:
            school[idx] = fishAge - 1
        else:
            school[idx] = 6
            extras.append(8) # New Fish
    
    if(extras):
        school = school.extend(extras)

for day in range(81):
    print("Day {} Count {}".format(day,len(initial)))
    doday(initial)





