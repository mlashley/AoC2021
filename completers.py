#!/usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import re

website="""
21   12400   6081  *****
20   16612    311  *****
19   11573    274  ****
18   19186    156  *****
17   26876   1274  *******
16   26994   1495  *******
15   32269   3088  ********
14   39452   6243  **********
13   44833    749  **********
12   43184   1666  **********
11   51274    242  ***********
10   57546   1503  *************
 9   56794   9053  *************
 8   61047  10853  ***************
 7   78499   2025  *****************
 6   79577   6092  ******************
 5   81387   3959  *****************
 4   92482   5218  ********************
 3  119497  31813  *******************************
 2  166512   6130  ***********************************
 1  185778  21701  *****************************************
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
