import pickle
import time
import sys
from Object import *
from twitter import *
import unicodedata
import json
import numpy as np

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
WW = np.zeros(shape=(6000, 6000))
PC = np.zeros(shape=(6000, 1))
PV = np.zeros(shape=(6000, 1))
iterr = 10
 
for i in range( len(userveri) ):
    PV[i] = 1

with open("WW.dump", "rb") as fp:   # Unpickling
    WW = pickle.load(fp)

if( 1 in WW[0] ): 
  print 'yo'

WW = np.array(WW)
PC = np.array(PC)
PV = np.array(PV)

for i in range(iterr):
    WWtemp = WW.transpose()
    PC = np.dot(WWtemp, PV)
    PV = np.dot(WW, PC)

indiV = np.argsort(PV)
indiC = np.argsort(PC)

ans = 0
coun = 0
for ind in indiV:
    if( coun>2000 ):
        break
    if( ind<len(userveri) ):  
        ans += 1
    coun += 1
    
print (ans/2000)