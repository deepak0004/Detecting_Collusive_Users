import seaborn as sns
import matplotlib.pyplot as plt
import pandas
import numpy as np
import time
from scipy import stats
import matplotlib as matpl
from textwrap import wrap
import sys

LIMIT_USERS = 100
NO_OF_USERS = 150
COLUMN_CONSI = int(sys.argv[1])
FLOATT = int(sys.argv[2])

mean = 0
dictt1 = []
dictt2 = []
filee = open('plotting_data2.txt', 'r')
oo = 0
maxx = 0
def func( val ):
    if( FLOATT==1 ):
       return float(splitted[COLUMN_CONSI])
    else:
       return int(splitted[COLUMN_CONSI])	

for line in filee:
  if( oo<LIMIT_USERS ):
     splitted = line.split(',')	
     dictt1.append( func(splitted[COLUMN_CONSI]) )
  else:
     splitted = line.split(',') 
     dictt2.append( func(splitted[COLUMN_CONSI]) )
  
  maxx = max(maxx, func(splitted[COLUMN_CONSI]))

  if( func(splitted[COLUMN_CONSI])!=-1 ):
     mean += func(splitted[COLUMN_CONSI])
  oo += 1

listtx = []
listtx2 = []
for i in range(LIMIT_USERS):
     listtx.append(i)
for i in range(LIMIT_USERS, NO_OF_USERS):
     listtx2.append(i)

fig = plt.figure()
plt.scatter(listtx, dictt1, marker='o', color='red')
plt.scatter(listtx2, dictt2, marker='o', color='green')
plt.ylabel('Value')
plt.xlabel('Interval')
fig = matpl.pyplot.gcf()
fig.set_size_inches(10, 7)

axes = plt.gca()
axes.set_ylim([-1, maxx])

st = 'Plots/acctosir'
plt.savefig(st + '.png')

avg = float(mean) / oo
print avg