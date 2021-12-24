#!/usr/bin/python3
import re

def translatefile(filename,input):
    
    inp = ( int(x) for x in input )
    w=0
    x=0
    y=0
    z=0
    for l in open(filename,"r").readlines():
        out = ""
        m = re.match(r"(\w+) (\w+) ?(.*)",l.strip())
        op,a,b = m.groups()
        # print(f"OP:{op} on {a} and {b}")
        if op == 'inp':
            out = next(inp) # hack - they are all w...
        elif op == 'add':
            out = eval(f"{a}+{b}")
        elif op == 'mul':
            out = eval(f"{a}*{b}")
        elif op == 'mod':
            out = eval(f"{a} % {b}")
        elif op == 'div':
            out = eval(f"{a} // {b}")
        elif op == 'eql':
            out = eval(f"int({a} == {b})")
        else:
            raise ValueError(f"Unhandled op-code {op} on {a} and {b}")
        
        if a == 'w':
            w=out
        elif a == 'x':
            x=out
        elif a == 'y':
            y=out
        elif a == 'z':
            z=out

        print(f"{l.strip()} => {out}\t[ w: {w} x: {x} y: {y} z:{z} ]")

    

translatefile("input","21")

# First input => input,1,input+6,input+6

# translatefile("input","12345678912345")


