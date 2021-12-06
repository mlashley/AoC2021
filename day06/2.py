#!/usr/bin/python3 

f = open("input","r")
# f = open("input.test","r")

initial = [ int(x) for x in f.readline().strip().split(',') ]

# We don't need to keep a list of individuals, you _are_ just a number...
# Also - the part1 solution doesn't scale to 1743335992042  (>2^40) elements ;-)

histo=[0]*9
for i in initial:
    histo[i] = histo[i] + 1

def doday(histo):
    out = [0]*9
    for age,count in enumerate(histo):
        if age > 0:
            out[age-1] += count
        else: # is zero
            out[8] = count  # New-born fish
            out[6] += count # New gestation period
    return out

for day in range(257):
     print("Day {} Count {} Histo {}".format(day,sum(histo),histo))
     histo=doday(histo)





