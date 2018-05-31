import pickle
import time
import sys
from twitter import *
import unicodedata
import json
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import xlsxwriter

SIZE_OF_MAT = 1000

with open("retweet_tweet_dictt.dump", "rb") as fp:   # Unpickling
    mat1 = pickle.load(fp)
'''
for i in range(SIZE_OF_MAT):
     mat1[i] = sorted(mat1[i])
     if( i>=600 and i<650 ):
	     for j in range(40):
	     	mat1[i][j] = 0 
print mat1[601]
'''
#print len(mat1)

us_list = []
inputt = open('total_users.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

coun = 0
for username in us_list:
    username = username.strip() 
    username = username.strip('\n')
    username = username.split('/')
    username = username[3]
    
    print username, " ", coun
    print mat1[username]
    coun += 1

'''
col = 0
for row, data in enumerate(mat1):
    worksheet.write_row(row, col, data)

workbook.close()
ax = sns.heatmap(mat1, linewidth=0.5)
plt.show()
#plt.imshow(mat1, cmap='hot', interpolation='nearest')
#plt.show()

#plt.imshow(mat2, cmap='hot', interpolation='nearest')
#plt.show()
'''