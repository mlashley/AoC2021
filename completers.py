#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
25    8453   4990  ***
24   10163    131  ***
23   10819   2268  ****
22   13205   5852  *****
21   17413   6043  ******
20   20315    339  *****
19   14495    255  ****
18   22332    160  ******
17   29886   1348  *******
16   29849   1518  *******
15   35145   3160  ********
14   42335   6512  **********
13   47850    800  **********
12   45944   1786  **********
11   54443    269  ************
10   60852   1579  *************
 9   59880   9612  **************
 8   64091  11354  ***************
 7   82269   2108  *****************
 6   83223   6326  ******************
 5   84929   4156  *****************
 4   96351   5490  *********************
 3  123981  32870  *******************************
 2  172278   6342  ***********************************
 1  191641  22431  *****************************************
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
