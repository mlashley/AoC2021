#!/usr/bin/python3
import logging
from functools import cache

#############
#...........#
###D#B#B#A###
  #C#C#D#A#
  #########


# We will use a tuple to serialize state
# A=1, B=2, C=3, D=4, 0=empty
# Series of numbers of positions as S1 S1, S2, S2, S3, S3, S4, S4, H1..11
# each pair of Sn is the lower,upper side-room position... in order
#
# e.g the starting state = (3,4,3,2,4,2,1,1,0,0,0,0,0,0,0,0,0,0,0)
# and the target state   = (1,1,2,2,3,3,4,4,0,0,0,0,0,0,0,0,0,0,0)

# We will serialize the current/best energy spends to an additional last two positions.

start = (3,4,3,2,4,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
teststart = (1,2,4,3,3,2,1,4,0,0,0,0,0,0,0,0,0,0,0,0,0)

# Part 2 adds 2 more rows... - so our room array [0:15] and hallway [16:26]

#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########


# Rules

# No stop immediately outside room => H3, H5, H7, H9 forbidden 
# or hallways=state[8:-1], hall[2,4,6,8]

# No entering room unless it is target room *and* only target amphipods present.

# Once in hallway - next stop has to be a room.
# (And that must be the target room due to rule 2...)

# Obvs - cannot pass thru others...

# For recursion - should not cost more than current best score.

# Part1
ENTRANCEIDX = (10,12,14,16) # Part1
COMPLETE=(1,1,2,2,3,3,4,4) # Part1
ROOMCOUNT = 8
SCOREOFF  = 19 # 19 part 1
ROOMROWS = 2

# Part2
#ENTRANCEIDX = (18,20,22,24)
#complete=(1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4)
#ROOMCOUNT = 16 # 8 part 1
#SCOREOFF  = 27 # 19 part 1
#ROOMROWS = 4


@cache
def nextStates(st):
    global best
    # printState(st)
    score = lambda a,moves : moves * (10**(a-1))
    hallindexoutsideroom = lambda a : (2*a)+ROOMCOUNT

    if st[:ROOMCOUNT] == COMPLETE:
        print("Finished score",st[SCOREOFF])
        if st[SCOREOFF] < best:
            logging.info(f"Finished new best score {st[SCOREOFF]}")
            best = st[SCOREOFF]
        else:
            logging.debug("Finished score {st[SCOREOFF]}")
        # printState(st)
        return []

    if st[SCOREOFF] > best:
        logging.debug(f"Abort {st[SCOREOFF]} larger {best}")
        return []

    ns = []
    for i,a in enumerate(st[0:SCOREOFF]):
        if(a>0): # Something to move?
            if i < ROOMCOUNT:  # Rooms

                # Don't move out of endpos...

                if i in range(0,ROOMCOUNT,2): # Bottom room
                    if i == 2*(a-1): # Target Room
                        logging.debug(f"a{a} at {i} in target room (lower)")
                        continue

                    if st[i+1]:  # No way out past...
                        logging.debug(f"a{a} at {i} no way out past {st[i+1]}")
                        continue

                    rmoves=2 # We step into the corridor
                    logging.debug(f"Possible Lower step into corridor for a{a} at idx:{i}")
                else: # Upper Rooms
                    # Here we must check we have not trapped another class below us...
                    if i-1 == 2*(a-1) and st[i-1] == a: # Target Room
                        logging.debug(f"a{a} at {i} in target room (upper)")
                        continue


                    rmoves=1 # We step into the corridor
                    logging.debug(f"Possible Upper step into corridor for a{a} at idx:{i}")

                hallindexoutside = hallindexoutsideroom((i//2)+1) # (a)
                # To the Left
                for hallpos in range(hallindexoutside-1,7,-1):
                    if st[hallpos] == 0 and hallpos not in ENTRANCEIDX:
                        newsta = [x for x in st]
                        newsta[hallpos] = a
                        newsta[i] = 0
                        newsta[SCOREOFF] += score(a,rmoves+(hallindexoutside-hallpos))
                        ns.append(tuple(newsta))
                    elif st[hallpos] != 0:
                        break # We are done...

                # To the Right
                # Note that we don't check the interim here because we are doing it incrementatlly and breaking.
                for hallpos in range(hallindexoutside+1,SCOREOFF):
                    logging.debug(f"a:{a} i:{i} hp:{hallpos} st:{st[hallpos]} h-i-outside{hallindexoutside}")
                    if st[hallpos] == 0 and hallpos not in ENTRANCEIDX:
                        newsta = [x for x in st]
                        newsta[hallpos] = a
                        newsta[i] = 0
                        newsta[SCOREOFF] += score(a,rmoves+(hallpos-hallindexoutside))
                        ns.append(tuple(newsta))
                    elif st[hallpos] != 0:
                        break # We are done...
                
                
            else: # i>=ROOMCOUNT => Corridor
                targethallidx = ROOMCOUNT + (a * 2) # 10,12,14,16 in world idx
                assert targethallidx in ENTRANCEIDX
                logging.debug(f"i:{i} Targethallindex: {targethallidx}")
                if ( i<targethallidx and not any(st[i+1:targethallidx+1]) ) or ( targethallidx<i and not any(st[targethallidx:i]) ) :
                    
                    if i<targethallidx:
                        moves = targethallidx-i
                    else:
                        moves = i-targethallidx
                    logging.debug(f"Clear to hall outside room i:{i} a:{a} in {moves} moves")
                    j = ROOMROWS*(a-1) # j is side-room-offset into state array, for given ammphi a is 1-based...
                    for k in range(0,ROOMROWS):
                        logging.debug(f"Check {st[j+k:j+ROOMROWS]} = {(0,)*(ROOMROWS-k)} for j:{j} k:{k} {ROOMROWS}")
                        if st[j+k:j+ROOMROWS] == (0,)*(ROOMROWS-k) and st[j:j+k] == (a,)*k: # If All above are empty _and_ all below are us.
                            logging.debug(f"Move to sideroom-{k} is valid")
                            rmoves = ROOMROWS-k
                            newsta = [x for x in st]
                            newsta[j+k] = a
                            newsta[i] = 0
                            newsta[SCOREOFF] += score(a,moves+rmoves) # Add score
                            ns.append(tuple(newsta))
    
    # if len(ns) == 0:
    #     print("==== NO MORE MOVES ==== ")
    #     printState(st)
    #     print("==== END NO MORE MOVES ==== ")

    # print(f"Score {st[SCOREOFF]} Looping {len(ns)} more")
    return [ nextStates(x) for x in ns ]

def printState(st):
    hall=st[ROOMCOUNT:SCOREOFF]
    siderooms = list(zip(st[0:ROOMCOUNT:2],st[1:ROOMCOUNT:2]))
    score=st[SCOREOFF]
    minscore=best
    halltxt="".join([str(x) if x>0 else "." for x in hall])
    sideroomuppertxt = "#".join([ str(r[1]) for r in siderooms ])
    sideroomlowertxt = "#".join([ str(r[0]) for r in siderooms ])

    halltxt = halltxt.replace("1","A").replace("2","B").replace("3","C").replace("4","D").replace("0",".")
    sideroomuppertxt = sideroomuppertxt.replace("1","A").replace("2","B").replace("3","C").replace("4","D").replace("0",".")
    sideroomlowertxt = sideroomlowertxt.replace("1","A").replace("2","B").replace("3","C").replace("4","D").replace("0",".")

    print(f"############# Score: {score}")
    print(f"#{halltxt}# Best:  {minscore}")
    print(f"###{sideroomuppertxt}###")
    print(f"  #{sideroomlowertxt}#  ")
    print(f"  #########\n\n{st}")

l = logging.getLogger()
l.setLevel(logging.DEBUG)
l.setLevel(logging.INFO)


# teststart=(1,0,4,0,3,0,1,4,0,0,0,2,0,0,0,2,0,3,0,0,0) # was broken
# teststart=(1,0,2,2,3,0,4,0,3,0,0,0,0,0,0,0,0,1,4,0,0) # easy

best=99999999
n=nextStates(teststart)
print(f"Test Best {best}")
assert best==12521


best=99999999
n=nextStates(start)
print(f"Part 1Best {best}")
assert best==15472



# Random interim unit-tests from partial implementation.

# t1=(1,1,2,2,3,0,4,0,3,0,0,0,0,0,0,0,0,0,4,0,0)
# t1=(1,0,2,2,3,0,4,0,3,0,0,0,0,1,0,0,0,0,4,0,0)
# print("From:")
# printState(t1)
# print("To:")
# for s in nextStates(t1):
#     printState(s)

# assert nextStates((1,1,2,2,3,0,4,0,3,0,0,0,0,0,0,0,0,0,4,0,0)) == [
# (1, 1, 2, 2, 3, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 700, 0),
# (1, 1, 2, 2, 3, 0, 4, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3000, 0)
# ]

# assert nextStates((1,0,2,2,3,0,4,0,3,0,0,0,0,1,0,0,0,0,4,0,0)) == [
# (1, 1, 2, 2, 3, 0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0),
# (1, 0, 2, 2, 3, 0, 4, 4, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3000, 0)
# ]

# assert nextStates((1,0,2,2,3,0,4,0,3,0,0,0,0,0,0,0,0,1,4,0,0)) == [
# (1, 0, 2, 2, 3, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 700, 0),
# (1, 1, 2, 2, 3, 0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 8, 0)
# ]

# t1=(1,0,2,2,3,0,4,0,3,0,0,0,0,0,0,1,0,0,4,0,0)

# print("From:")
# printState(t1)
# print("To:")
# for s in nextStates(t1):
#     printState(s)


