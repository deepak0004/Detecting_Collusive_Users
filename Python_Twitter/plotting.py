import seaborn as sns
import matplotlib.pyplot as plt
import pandas
import numpy as np
import time
from scipy import stats
import matplotlib as matpl
from textwrap import wrap
import sys

NO_OF_USERS = 150
COLUMN_CONSI = int(sys.argv[1])
FLOATT = int(sys.argv[2])

coun = 0
mean = 0
dictt = {}
filee = open('plotting_data.txt', 'r')

def func( val ):
    if( FLOATT==1 ):
       return float(splitted[COLUMN_CONSI])
    else:
       return int(splitted[COLUMN_CONSI])	

for line in filee:
   splitted = line.split(',')	
   if( coun in dictt ):
   	  dictt[coun].append( func(splitted[COLUMN_CONSI]) )
   else: 
      dictt[coun] = [ func(splitted[COLUMN_CONSI]) ]
   coun += 1
   coun %= NO_OF_USERS
   mean += func(splitted[COLUMN_CONSI])

for i in range(NO_OF_USERS):
    listtx = []
    for j in range( len(dictt[i]) ):
        listtx.append(j)

    fig = plt.figure()
    plt.plot(listtx, dictt[i], marker='o')
    plt.ylabel('Value')
    plt.xlabel('Interval')
    fig = matpl.pyplot.gcf()
    fig.set_size_inches(10, 7)
    
    st = 'Plots/' + str(i)
    plt.savefig(st + '.png')

avg = float(mean) / NO_OF_USERS
print avg