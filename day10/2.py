#!/usr/bin/python3 

f = open("input","r")
# f = open("input.test","r")

opening = [ '(', '[', '{', '<', 'S'] # S and E are my start and end markers (^$)
closing = [ ')', ']', '}', '>', 'E']

def parse(l,lastopen):

    if l[0] == "E":
        # print("Parsed to End == Incomplete")
        return False
    closer = closing[opening.index(lastopen)]
    # print(f"Parsing {l} with {lastopen} {closer}")   
    if l[0] in closing:
        if l[0] == closer:
            print("Normal Close")
            return True
        else:
            # print("Syntax Error - Expected {} got {}".format(closer,l[0]))
            return None
    if l[0] in opening:
        return parse(l[1:],l[0])

def simplify(l):
    t = l.replace('<>','').replace('[]','').replace('()','').replace('{}','')
    if(len(t) < len(l)):
        return simplify(t) # Keep trying
    else:
        return(t) # Done

def complete(l):
    comp=[]
    score = 0
    for x in l[::-1]:
        i = opening.index(x)
        comp.append(closing[i])
        score = ( score * 5 ) + (i+1)
    # print("".join(comp),score)
    return(score)

scores=[]
for line in f.readlines():
    l = simplify(line.strip())
    x=parse(f"{l}E",'S')
    # print(f"Simplified {l} from {line.strip()} {x}")
    if x == False: # Incomplete
        scores.append(complete(l))

scores.sort()
mid = int((len(scores) - 1 ) / 2)
print(f"Part2 Score: {scores[mid]}")