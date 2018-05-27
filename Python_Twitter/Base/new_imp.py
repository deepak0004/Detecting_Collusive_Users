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

'''
st = sys.argv[1]
print st
config = {}
execfile(st, config)
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
userveri = []
usercust = []
us_list = []

with open("userveri.dump", "rb") as fp:   # Unpickling
    userveri = pickle.load(fp)

with open("usercust.dump", "rb") as fp:   # Unpickling
    usercust = pickle.load(fp)

with open("dictt1.dump", "rb") as fp:   # Unpickling
    dictt1 = pickle.load(fp)

with open("dictt2.dump", "rb") as fp:   # Unpickling
    dictt2 = pickle.load(fp)

with open("dictt3.dump", "rb") as fp:   # Unpickling
    dictt3 = pickle.load(fp)

with open("dictt4.dump", "rb") as fp:   # Unpickling
    dictt4 = pickle.load(fp)

dictt = dict(dictt1.items() + dictt2.items() + dictt3.items() + dictt4.items())

usercust = usercust[:2000]
userveri = userveri[:4000]

def func(us1, us2):
   if( us1<len(userveri) ):
       name1 = userveri[us1]
   else:
       name1 = usercust[us1 - len(userveri)] 
   if( us2<len(userveri) ):
       name2 = userveri[us2]
   else:
       name2 = usercust[us2 - len(userveri)] 
   return name1, name2

userss = userveri
users.extend(usercust)
'''

def func(us1, us2):
  flag = 0
  while(flag==0):
    try:
        consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
        twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
        result = twitter.friendships.show(source_screen_name = us1, target_screen_name = us2)
        if( result["relationship"]["target"]["following"]==us2 ):
           return 1
        return 0 
    except Exception as e:
        print e
        print 'yo1'
        stst = ''
        flag3 = 0
        for pp in e[0]:
            if( pp=='{' or flag3 == 1 ):
               stst += pp
               flag3 = 1

        stst = stst.split(':')
        if( len(stst)>=4 ):
            op =  stst[3][1] + stst[3][2]
            print op
            if( op == "88" ):
                time.sleep(60)
                continue
        flag = 1 
    return 0

cust = 300
iterr = 10
us_list = []
us_cust = []
usercust = []
users = 0

#cust = 5

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
   print us1
   for us2 in range( users ):
      o1 = usercust[us1]
      o2 = usercust[us2]
      if( o1!=o2 and func(o1, o2)==1 ): 
           WW[us1][us2] = 1
           print 'meeeee'
   if( (us1%100)==0 ):
     with open('WW.dump', "wb") as fp: 
        pickle.dump(WW, fp)

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

print PV
print indiV

ytrue = []
ypred = []
ans = 0
for i in range(users):
    if( i<cust ):
      ytrue.append(1)
    else:
      ytrue.append(0)
for ind in indiV:
    print ind
    if( ind<cust ):  
      ans += 1
      ypred.append(1)
    else:
      ypred.append(0)
    
print 'Ans: ', (float(ans)/users)

print 'ypred ', ypred
print 'ytrue ', ytrue

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