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

with open("dictt_retweet_follo2.dump", "rb") as fp:   # Unpickling
    mat1 = pickle.load(fp)

SIZE_OF_MAT = 1000
pp = 0
#mat2 = np.zeros(shape=(40, 100)) 
'''
for i in range(SIZE_OF_MAT):
     if( i<20 ):
         for j in range(100):
            mat2[pp][j] = mat1[i][j]
         pp += 1
     if( i>=500 and i<520 ):
         for j in range(100):
            mat2[pp][j] = mat1[i][j] 
         pp += 1
print pp
'''

#print len(mat1)
mat2 = {}
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
    if( coun<20 ):
        mat2[username] = mat1[username]
        pp += 1
    if( coun>=500 and coun<520 ):
        mat2[username] = mat1[username]
        pp += 1

    coun += 1

#col = 0
'''
for row, data in enumerate(mat1):
    worksheet.write_row(row, col, data)

workbook.close()
ax = sns.heatmap(mat1, linewidth=0.5)
plt.show()
'''
#plt.imshow(mat1, cmap='hot', interpolation='nearest')
#plt.show()

#plt.imshow(mat2, cmap='hot', interpolation='nearest')
#plt.show()

with open('Retweet_Ratio.dump', "wb") as fp: 
    pickle.dump(mat2, fp)

print mat2['abhisheksapabap']
#print mat2[]