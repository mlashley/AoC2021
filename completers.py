#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
23    5127   2987  **
22   10136   6160  ****
21   15091   5950  *****
20   18172    323  *****
19   12619    271  ****
18   20330    166  *****
17   27927   1313  *******
16   27941   1487  *******
15   33172   3077  ********
14   40298   6333  **********
13   45736    763  **********
12   43987   1704  **********
11   52193    245  ***********
10   58557   1532  *************
 9   57724   9271  **************
 8   61971  11032  ***************
 7   79624   2078  *****************
 6   80676   6176  ******************
 5   82429   4022  *****************
 4   93658   5287  ********************
 3  120865  32151  *******************************
 2  168285   6220  ***********************************
 1  187588  21969  *****************************************
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
