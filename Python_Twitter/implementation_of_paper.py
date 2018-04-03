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

userss = userveri
users.extend(usercust)
WW = np.zeros(shape=(6000, 6000))
PC = np.zeros(shape=(6000, 1))
PV = np.zeros(shape=(6000, 1))
iterr = 10
 
for i in range( len(userveri) ):
    PV[i] = 1

for us1 in range( len(users) ):
   for us2 in range( len(users) ):
      if( us1!=us2 ):
          WW[us1][us2] = op
    
with open("WW.dump", "wb") as fp:  
    pickle.dump(WW, fp)    

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