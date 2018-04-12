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

SIZE_OF_MAT = 100
workbook = xlsxwriter.Workbook('mat1.xlsx')
worksheet = workbook.add_worksheet()

with open("mat1.dump", "rb") as fp:   # Unpickling
    mat1 = pickle.load(fp)
#with open("mat2.dump", "rb") as fp:   # Unpickling
#    mat2 = pickle.load(fp)

for i in range(SIZE_OF_MAT):
     mat1[i] = sorted(mat1[i])
'''
for i in range(SIZE_OF_MAT):
     mat1[i] = sorted(mat1[i])
     su = 0
     for j in range(SIZE_OF_MAT):
       su += mat1[i][j]
     for j in range(SIZE_OF_MAT):
       mat1[i][j] = float(mat1[i][j])/su	
'''

col = 0
for row, data in enumerate(mat1):
    worksheet.write_row(row, col, data)

workbook.close()
'''
ax = sns.heatmap(mat1, linewidth=0.5)
plt.show()
'''
#plt.imshow(mat1, cmap='hot', interpolation='nearest')
#plt.show()

#plt.imshow(mat2, cmap='hot', interpolation='nearest')
#plt.show()