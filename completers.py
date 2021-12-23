#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
22    8522   6537  ****
21   14470   5837  *****
20   17672    304  *****
19   12293    266  ****
18   19925    167  *****
17   27543   1286  *******
16   27602   1496  *******
15   32839   3051  ********
14   39980   6280  **********
13   45370    756  **********
12   43655   1696  **********
11   51835    244  ***********
10   58153   1518  *************
 9   57358   9178  *************
 8   61604  10970  ***************
 7   79183   2062  *****************
 6   80257   6142  ******************
 5   82047   3974  *****************
 4   93195   5243  ********************
 3  120330  32051  *******************************
 2  167599   6195  ***********************************
 1  186907  21883  *****************************************
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
