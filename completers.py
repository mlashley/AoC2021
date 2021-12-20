#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
19    7488    300  ***
18   16212    204  *****
17   24829   1260  ******
16   25346   1468  ******
15   30836   3050  ********
14   38128   6131  **********
13   43566    713  **********
12   42040   1619  **********
11   49985    228  ***********
10   56225   1454  ************
 9   55597   8891  *************
 8   59841  10673  ***************
 7   77030   1975  *****************
 6   78177   6001  ******************
 5   80033   3905  *****************
 4   91053   5083  *******************
 3  117743  31301  *******************************
 2  164110   6019  ***********************************
 1  183250  21405  *****************************************
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
