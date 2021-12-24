#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
23    6421   2831  ***
22   10450   6126  ****
21   15281   5947  *****
20   18329    318  *****
19   12744    270  ****
18   20443    163  *****
17   28046   1310  *******
16   28066   1502  *******
15   33283   3077  ********
14   40427   6364  **********
13   45876    760  **********
12   44109   1703  **********
11   52328    252  ***********
10   58715   1535  *************
 9   57862   9284  **************
 8   62111  11023  ***************
 7   79762   2084  *****************
 6   80808   6194  ******************
 5   82589   4018  *****************
 4   93819   5306  ********************
 3  121052  32201  *******************************
 2  168504   6221  ***********************************
 1  187806  21997  *****************************************
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
