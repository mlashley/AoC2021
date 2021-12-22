#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
22    4959   6542  ***
21   13722   5857  *****
20   17166    298  *****
19   11935    259  ****
18   19525    179  *****
17   27194   1276  *******
16   27289   1479  *******
15   32536   3073  ********
14   39687   6265  **********
13   45077    755  **********
12   43394   1695  **********
11   51526    251  ***********
10   57830   1500  *************
 9   57051   9105  *************
 8   61298  10896  ***************
 7   78831   2054  *****************
 6   79924   6100  ******************
 5   81680   3972  *****************
 4   92790   5229  ********************
 3  119876  31934  *******************************
 2  167015   6157  ***********************************
 1  186294  21791  *****************************************
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
