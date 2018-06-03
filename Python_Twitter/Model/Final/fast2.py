import pickle
import time
import sys
from twitter import *
import unicodedata
import json
import numpy as np
import api_settings
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix, roc_curve, roc_auc_score, auc

settings_file =  "apikeys/apikeys.txt"
history_file = "apikeys/api_history.txt"

with open("dictt.dump", "rb") as fp:   # Unpickling
    dictt = pickle.load(fp)

cust = 300
iterr = 10
us_list = []
usercust = []
users = 0

inputt = open('total_users.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

for username in us_list:
    users += 1
    username = username.strip() 
    username = username.strip('\n')
    username = username.split('/')
    username = username[3]

    usercust.append(username)

WW = np.zeros(shape=(users, users))
PC = np.zeros(shape=(users, 1))
PV = np.zeros(shape=(users, 1))
for i in range(cust):
    PV[i] = 1

for us1 in range( users ):
   print( us1 )
   for us2 in range( users ):
      o1 = usercust[us1]
      o2 = usercust[us2]
      if( (o1!=o2) and (o2 in dictt[o1]) ): 
           WW[us1][us2] = 1
           print( 'meeeee' )

with open('WW.dump', "wb") as fp: 
   pickle.dump(WW, fp)

WW = np.array(WW)
PC = np.array(PC)
PV = np.array(PV)

for i in range(iterr):
    WWtemp = WW.transpose()
    PC = np.dot(WWtemp, PV)
    PV = np.dot(WW, PC)

PV = np.reshape(PV, users)
PC = np.reshape(PC, users)

indiV = np.argsort(PV)
indiC = np.argsort(PC)

print( PV )
print( indiV )

ytrue = []
ypred = []
ans = 0
for i in range(users):
    if( i<cust ):
      ytrue.append(1)
    else:
      ytrue.append(0)
for ind in indiV:
    print( ind )
    if( ind<cust ):  
      ans += 1
      ypred.append(1)
    else:
      ypred.append(0)
    
print( 'Ans: ', (float(ans)/users) )

print( 'ypred ', ypred )
print( 'ytrue ', ytrue )

fpr, tpr, thresholds = roc_curve(ytrue, ypred, pos_label=2)

print(f1_score(ytrue, ypred, average="macro"))
print(precision_score(ytrue, ypred, average="macro"))
print(recall_score(ytrue, ypred, average="macro"))    
print(roc_auc_score(ytrue, ypred, average="macro"))

print(f1_score(ytrue, ypred, average="micro"))
print(precision_score(ytrue, ypred, average="micro"))
print(recall_score(ytrue, ypred, average="micro"))    
print(roc_auc_score(ytrue, ypred, average="micro"))

print(auc(fpr, tpr))