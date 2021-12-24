#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
24    2446    139  **
23    7197   2739  ***
22   10702   6118  *****
21   15452   5966  *****
20   18492    327  *****
19   12871    266  ****
18   20581    169  *****
17   28182   1309  *******
16   28184   1501  *******
15   33398   3087  ********
14   40550   6369  **********
13   46007    760  **********
12   44223   1699  **********
11   52452    251  ***********
10   58830   1545  *************
 9   57980   9300  **************
 8   62228  11068  ***************
 7   79909   2080  *****************
 6   80955   6207  ******************
 5   82735   4029  *****************
 4   93982   5315  ********************
 3  121231  32271  *******************************
 2  168761   6224  ***********************************
 1  188077  22005  *****************************************
"""
a = website.split('\n')
a.reverse()

day=[]
twostar=[]
onestar=[]

for line in a:
    # m=re.match(r"\s+(\d+)\s+(\d+)\s+(d+).*",line)
    m=re.match(r"\s?(\d+)\s+(\d+)\s+(\d+)",line)
    if m:
        print(m.group(1),m.group(2),m.group(3))
        day.append(int(m.group(1)))
        twostar.append(int(m.group(2)))
        onestar.append(int(m.group(3)))

plt.scatter(day,twostar)
plt.scatter(day,onestar,c="grey")
plt.savefig("./userprogress.png")
plt.show()
