#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
21   10697   6389  *****
20   16143    338  *****
19   11273    280  ****
18   18932    159  *****
17   26641   1307  *******
16   26832   1476  *******
15   32116   3074  ********
14   39289   6231  **********
13   44692    749  **********
12   43040   1671  **********
11   51113    241  ***********
10   57382   1494  *************
 9   56651   9023  *************
 8   60905  10836  ***************
 7   78331   2029  *****************
 6   79432   6066  ******************
 5   81204   3945  *****************
 4   92278   5210  ********************
 3  119274  31756  *******************************
 2  166217   6105  ***********************************
 1  185467  21676  *****************************************
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
