#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
18   12151    249  ****
17   23228   1298  ******
16   24090   1475  ******
15   29806   3105  *******
14   37302   6107  **********
13   42772    715  **********
12   41383   1598  **********
11   49306    224  ***********
10   55516   1433  ************
 9   54968   8778  *************
 8   59138  10618  ***************
 7   76223   1953  ****************
 6   77399   5968  ******************
 5   79240   3869  *****************
 4   90260   5052  *******************
 3  116806  31110  ******************************
 2  162950   5994  ***********************************
 1  182057  21311  *****************************************
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
