#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
19    5178    308  ***
18   15144    227  ****
17   24321   1296  ******
16   24947   1480  ******
15   30485   3074  *******
14   37835   6115  **********
13   43298    724  **********
12   41820   1611  **********
11   49747    228  ***********
10   55992   1452  ************
 9   55380   8852  *************
 8   59568  10681  ***************
 7   76734   1982  *****************
 6   77900   5972  ******************
 5   79709   3908  *****************
 4   90765   5088  *******************
 3  117405  31235  ******************************
 2  163700   6015  ***********************************
 1  182828  21386  *****************************************
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
