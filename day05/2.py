#!/usr/bin/python3 
import re
from PIL import Image, ImageDraw
import numpy as np

f = open("input","r")
WIDTH=1000
HEIGHT=1000

# f = open("input.test","r")
# WIDTH=10
# HEIGHT=10

base = Image.new("RGBA",(WIDTH,HEIGHT),color=(0,0,0,255))

# Smush the input data => pairs of strings => pairs of tuples
p1 = [ re.split(' -> ',x.strip()) for x in f.readlines()]
p2 = [ [ tuple(map(int,x[0].split(','))), tuple(map(int,x[1].split(','))) ] for x in p1]

# p2 is an array of lines [ tuple(startx,y), tuple(endx,y) ]
print(p2)

# Exactly identical to part1, only with the code to remove diagonals taken out :)
for line in p2:
    im = Image.new("RGBA",(WIDTH,HEIGHT),color=0)
    draw = ImageDraw.Draw(im)
    draw.line(line,fill=(255,255,255,127)) #,fil=None,width=1,joint=None)
    base=Image.alpha_composite(base,im)

base.show()

# Take the 'R' from RGBA and make a numpy-array to histogram..
pix = np.array(base.split()[0].getdata()).reshape(base.size[0], base.size[1])
# print(pix)

# Because we alpha-overed lines of RGBA(255,255,255,127) onto a black base, 
# eveything over 128 is hist >1 times, and counts to our answer.
hist = np.histogram(pix,bins=[0,128,256])
print(hist)

print("Points of overlap",hist[0][1])


