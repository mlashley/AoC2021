#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
22    3500   5875  ***
21   13439   5896  *****
20   17010    304  *****
19   11841    258  ****
18   19443    171  *****
17   27090   1277  *******
16   27198   1485  *******
15   32451   3075  ********
14   39616   6245  **********
13   45015    751  **********
12   43330   1675  **********
11   51440    249  ***********
10   57721   1500  *************
 9   56961   9092  *************
 8   61219  10873  ***************
 7   78738   2036  *****************
 6   79812   6099  ******************
 5   81598   3970  *****************
 4   92692   5213  ********************
 3  119745  31894  *******************************
 2  166844   6148  ***********************************
 1  186112  21779  *****************************************
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
