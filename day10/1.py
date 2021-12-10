#!/usr/bin/python3 

f = open("input","r")
# f = open("input.test","r")

opening = [ '[', '(', '<', '{', 'S'] # S and E are my start and end markers (^$)
closing = [ ']', ')', '>', '}', 'E']

def score(c):
    if c == ')':
        score.value += 3
    elif c == ']':
        score.value += 57
    elif c == '}':
        score.value += 1197
    elif c == '>':
        score.value += 25137
score.value = 0

def parse(l,lastopen):

    if l[0] == "E":
        print("Parsed to End == Incomplete")
        return
    
    closer = closing[opening.index(lastopen)]
    # print(f"Parsing {l} with {lastopen} {closer}")   
    if l[0] in closing:
        if l[0] == closer:
            print("Normal Close")
            return
        else:
            print("Syntax Error - Expected {} got {}".format(closer,l[0]))
            score(l[0])
    if l[0] in opening:
        parse(l[1:],l[0])

def simplify(l):
    t = l.replace('<>','').replace('[]','').replace('()','').replace('{}','')
    if(len(t) < len(l)):
        return simplify(t) # Keep trying
    else:
        return(t) # Done

for line in f.readlines():

    l = simplify(line.strip())
    print(f"Simplified {l} from {line}")
    parse(f"{l}E",'S')

print("Score: ",score.value)