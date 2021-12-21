#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
21    7603   6125  ****
20   15583    336  *****
19   10979    269  ****
18   18629    154  *****
17   26387   1281  *******
16   26602   1479  *******
15   31925   3070  ********
14   39100   6207  **********
13   44506    740  **********
12   42875   1668  **********
11   50930    236  ***********
10   57192   1479  *************
 9   56453   8985  *************
 8   60698  10803  ***************
 7   78075   2022  *****************
 6   79221   6076  ******************
 5   81018   3922  *****************
 4   92070   5173  ********************
 3  118999  31641  *******************************
 2  165818   6097  ***********************************
 1  185075  21646  *****************************************
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
