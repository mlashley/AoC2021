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


# Rules

# No stop immediately outside room => H3, H5, H7, H9 forbidden 
# or hallways=state[8:-1], hall[2,4,6,8]

# No entering room unless it is target room *and* only target amphipods present.

# Once in hallway - next stop has to be a room.
# (And that must be the target room due to rule 2...)

# Obvs - cannot pass thru others...

# For recursion - should not cost more than current best score.

entrancesIdx = (10,12,14,16)

@cache
def nextStates(st):
    global best
    # printState(st)
    score = lambda a,moves : moves * (10**(a-1))
    hallindexoutsideroom = lambda a : (2*a)+8

    if st[:8] == (1,1,2,2,3,3,4,4):
        print("Finished score",st[19])
        if st[19] < best:
            logging.info("Finished new best score",st[19])
            best = st[19]
        else:
            logging.debug("Finished score",st[19])
        printState(st)       
        return []

    if st[19] > best:
        logging.debug(f"Abort {st[19]} larger {best}")
        return []

    ns = []
    for i,a in enumerate(st[0:19]): 
        if(a>0): # Something to move?
            if i < 8:  # Rooms

                # Don't move out of endpos...

                if i in (0,2,4,6): # Bottom room
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
                    if st[hallpos] == 0 and hallpos not in entrancesIdx:
                        newsta = [x for x in st]
                        newsta[hallpos] = a
                        newsta[i] = 0
                        newsta[19] += score(a,rmoves+(hallindexoutside-hallpos))
                        ns.append(tuple(newsta))
                    elif st[hallpos] != 0:
                        break # We are done...

                # To the Right
                # Note that we don't check the interim here because we are doing it incrementatlly and breaking.
                for hallpos in range(hallindexoutside+1,19):
                    logging.debug(f"a:{a} i:{i} hp:{hallpos} st:{st[hallpos]} h-i-outside{hallindexoutside}")
                    if st[hallpos] == 0 and hallpos not in entrancesIdx:
                        newsta = [x for x in st]
                        newsta[hallpos] = a
                        newsta[i] = 0
                        newsta[19] += score(a,rmoves+(hallpos-hallindexoutside))
                        ns.append(tuple(newsta))
                    elif st[hallpos] != 0:
                        break # We are done...
                
                
            else: # i>=8 => Corridor 
                targethallidx = 8 + (a * 2) # 10,12,14,16 in world idx
                assert targethallidx in entrancesIdx
                logging.debug(f"i:{i} Targethallindex: {targethallidx}")
                if ( i<targethallidx and not any(st[i+1:targethallidx+1]) ) or ( targethallidx<i and not any(st[targethallidx:i]) ) :
                    
                    if i<targethallidx:
                        moves = targethallidx-i
                    else:
                        moves = i-targethallidx
                    logging.debug(f"Clear to hall outside room {i} {a} in {moves} moves")
                    j = 2*(a-1) # j is side-room-offset into state array, for given ammphi a is 1-based...
                    if st[j] == 0 and st[j+1]==0:
                        logging.debug(f"Move to sideroom-low is valid")
                        moves += 2
                        newsta = [x for x in st]
                        newsta[j] = a
                        newsta[i] = 0       
                        newsta[19] += score(a,moves) # Add score
                        ns.append(tuple(newsta))
                    elif st[j] == a and st[j+1]==0:     
                        logging.debug(f"Move to sideroom-high is valid")
                        moves += 1
                        newsta = [x for x in st]
                        newsta[j+1] = a
                        newsta[i] = 0
                        newsta[19] += score(a,moves)
                        ns.append(tuple(newsta))
    
    # if len(ns) == 0:
    #     print("==== NO MORE MOVES ==== ")
    #     printState(st)
    #     print("==== END NO MORE MOVES ==== ")

    # print(f"Score {st[19]} Looping {len(ns)} more")
    return [ nextStates(x) for x in ns ]

def printState(st):
    hall=st[8:19]
    siderooms = list(zip(st[0:8:2],st[1:8:2]))
    score=st[19]
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
assert best==12521 
print(f"Test Best {best}")

best=99999999
n=nextStates(start)
print(f"Part 1Best {best}")



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


