#!/usr/bin/python3 
import math

f = open("input","r")
# f = open("input.test","r")

lines = f.readlines()
bits=len(lines[0])-1

bitcounts=[0] * (bits)

print("Found {} bits".format(bits))

total=len(lines)

def findlargestsubset(bit,arr):
    print("Searching bit {} in {} values".format(bit,len(arr)))
    ones = []
    zeros = []
    for elem in arr:
        if elem[bit] == "1":
            ones.append(elem)
        else:
            zeros.append(elem)

    print("Bit {} Ones {} Zeros {}".format(bit,len(ones),len(zeros)))

    if len(ones) >= len(zeros):
        print("Answer for bit {} is 1".format(bit))
        if len(ones) > 1:
            return findlargestsubset(bit+1,ones)
        else:
            return ones
    else:
        print("Answer for bit {} is 0".format(bit))
        if len(zeros) > 1:
            return findlargestsubset(bit+1,zeros)
        else:
            return(zeros)

def findsmallesestsubset(bit,arr):
    print("Searching bit {} in {} values".format(bit,len(arr)))
    ones = []
    zeros = []
    for elem in arr:
        if elem[bit] == "1":
            ones.append(elem)
        else:
            zeros.append(elem)

    if len(zeros) <= len(ones):
        print("Bit {} Zeros {} <= Ones {} => answer is 0".format(bit,len(zeros),len(ones)))
        if len(zeros) > 1:
            return findsmallesestsubset(bit+1,zeros)
        else:
            return(zeros)
    else:
        print("Bit {} Zeros {} > Ones {} => answer is 1".format(bit,len(zeros),len(ones)))
        if len(ones) > 1:
            return findsmallesestsubset(bit+1,ones)
        else:
            return ones

oxygen = int(findlargestsubset(0,lines)[0],2)
co2 = int(findsmallesestsubset(0,lines)[0],2)
print("Oxy {} CO2 {} Life Support {}".format(oxygen,co2,oxygen*co2))

