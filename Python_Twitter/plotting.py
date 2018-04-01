import seaborn as sns
import matplotlib.pyplot as plt
import pandas
import numpy as np
import time
from scipy import stats
import matplotlib as matpl
from textwrap import wrap
import sys

NO_OF_USERS = 26
COLUMN_CONSI = int(sys.argv[1])
FLOATT = int(sys.argv[2])

coun = 0
mean = 0
dictt = {}
#filee = open('plotting_data2.txt', 'r')
filee = open('plotting_datasmall.txt', 'r')

def func( val ):
    if( FLOATT==1 ):
       return float(splitted[COLUMN_CONSI])
    else:
       return int(splitted[COLUMN_CONSI])	

oo = 0
for line in filee:
   splitted = line.split(',')	
   if( coun in dictt ):
   	  dictt[coun].append( func(splitted[COLUMN_CONSI]) )
   else: 
      dictt[coun] = [ func(splitted[COLUMN_CONSI]) ]
   coun += 1
   coun %= NO_OF_USERS
   if( func(splitted[COLUMN_CONSI])!=-1 ):
       mean += func(splitted[COLUMN_CONSI])
   #print func(splitted[COLUMN_CONSI]) 
   oo += 1

#print 'coun: ', coun
#print 'oo: ', oo

for i in range(NO_OF_USERS):
    listtx = []
    for j in range( len(dictt[i]) ):
        listtx.append(j)

    #print 'dictt[i]: ', dictt[i] 

    fig = plt.figure()
    plt.plot(listtx, dictt[i], marker='o')
    plt.ylabel('Value')
    plt.xlabel('Interval')
    fig = matpl.pyplot.gcf()
    fig.set_size_inches(10, 7)
    
    st = 'Plots/' + str(i)
    plt.savefig(st + '.png')

avg = float(mean) / oo
print avg