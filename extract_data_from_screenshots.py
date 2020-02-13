import cv2
import numpy as np
from string import ascii_lowercase, digits
from operator import itemgetter
import re

img = cv2.imread('F:\\github\\Mumbai_Local_Train\\screenshots\\img.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

pos = set()

for alpha in list(ascii_lowercase) + list(digits) + [f'p{n}' for n in '1234']:
  if alpha in 'fqxz':
    continue
  small = cv2.imread(f'F:\\github\\Mumbai_Local_Train\\templates\\{alpha}.jpg')
  small_gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
  res = cv2.matchTemplate(img_gray, small_gray, cv2.TM_CCOEFF_NORMED)
  threshold = 0.95
  loc = np.where(res >= threshold)
  for pt in zip(*loc[::-1]):
    pos.add((alpha, pt[0] // 10 * 10, pt[1] // 10 * 10))


pos = list(pos)
pos.sort(key=itemgetter(1))
pos.sort(key=itemgetter(2))
print(*pos, sep='\n')

y = -1
s = []

for i in pos:
  if i[2] != y:
    if y != -1:
      print(*s, sep='')
      s = []
    y = i[2]
  s.append(i[0])
print(*s, sep='')