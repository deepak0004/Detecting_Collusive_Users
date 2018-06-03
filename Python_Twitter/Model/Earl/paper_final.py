import pickle
import time
import sys
import numpy as np
from twitter import *
from Object import *
import unicodedata
import json
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation
from scipy.spatial.distance import cdist
from scipy.spatial import distance
import math
import random
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix, roc_curve, roc_auc_score, auc

def normalize(v):
    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

dictt = {}
No_Of_Users = 100
cust_users = 50
total_topics = 100
latent_leng = 10
iterr = 1
betau = 0.3
betaw = 0.7
alphap = 0.4
alphaq = 0.4
alphar = 0.4
lambdau = 0.4
lambdav = 3

print 'alphap: ', alphap
print 'alphaq: ', alphaq
print 'alphar: ', alphar
print 'lambdau: ', lambdau
print 'lambdav: ', lambdav
print 'k: ', latent_leng

matu_f = np.zeros(shape=(No_Of_Users, total_topics))  
AA = np.zeros(shape=(No_Of_Users, No_Of_Users))
BB = np.zeros(shape=(No_Of_Users, No_Of_Users))
CC = np.zeros(shape=(No_Of_Users, No_Of_Users))
simimat = np.zeros(shape=(No_Of_Users, No_Of_Users))
maxxmat = np.zeros(shape=(No_Of_Users, 1))
'''
learnedu = np.zeros(shape=(No_Of_Users, latent_leng))       # U*k
learnedt = np.zeros(shape=(total_topics, latent_leng))      # T*k 
'''
learnedu = np.random.rand(No_Of_Users, latent_leng)    # U*k
learnedt = np.random.rand(total_topics, latent_leng)   # T*k 

#print 'Learnedu: ', learnedu
#print 'Learnedt: ', learnedt

def diff(i, j):
   o1 = learnedu[i]
   o2 = learnedu[j]
   subb = o1 - o2
   subb = (AA[i][j]*subb)
   return subb
def diff2(i, j):
   o1 = learnedu[i]
   o2 = learnedu[j]
   subb = o1 - o2
   subb = (BB[i][j]*subb)
   return subb
def diff3(i, j):
   o1 = learnedu[i]
   o2 = learnedu[j]
   subb = o1 - o2
   subb = (CC[i][j]*subb)
   return subb
def frob(i, j):
   o1 = learnedu[i]
   o2 = learnedu[j]
   anss = 0
   for p in range(latent_leng):
       anss += abs( float(o1[p] - o2[p])*(o1[p] - o2[p]) )
   #print anss
   anss = (1.0/(1+anss))
   #print anss
   return anss
def maxx(vect):
   ko = 0.0
   for j in range(len(vect)):
      #print 'vect[j]: ', vect[j]
      ko = max(ko, vect[j])
   #print 'vect: ', vect
   return ko

us_list = []
inputt = open('total_users.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

with open('ICDM/matu_f.dump', "rb") as fp: 
    matu_f = pickle.load(fp)
with open("ICDM/retweet_tweet_dictt.dump", "rb") as fp:  
    retweet_tweet_dictt = pickle.load(fp)
with open("ICDM/mapp_username_list24.dump", "rb") as fp:  
    mapp_username_list = pickle.load(fp)
with open("ICDM/dictt_retweet_follo.dump", "rb") as fp:  
    dictt_retweet_follo = pickle.load(fp)

for i in range(No_Of_Users):
  su = 1
  for j in range(100):
     su += matu_f[i][j]
  for j in range(100):
     matu_f[i][j] = float(matu_f[i][j])/su 

us_list = []
inputt = open('total_users.txt', 'r')
for line in inputt:
    username = line.strip() 
    username = username.strip('\n')
    username = username.split('/')
    username = username[3]
    us = str(username) 
    us_list.append(us) 

for i in range(No_Of_Users):
    for j in range(No_Of_Users):
      us1 = us_list[i]
      us2 = us_list[j]
      o1 = retweet_tweet_dictt[us1]
      o2 = retweet_tweet_dictt[us2]
      o3 = mapp_username_list[us1]
      o4 = mapp_username_list[us2]
      o5 = dictt_retweet_follo[us1]
      o6 = dictt_retweet_follo[us2]

      aa = 1.0 - min(o1, o2)
      bb = 1.0 - min(o3, o4)
      cc = max(o5, o6)

      o1 = 1.0 - math.exp( -aa )
      o2 = 1.0 - math.exp( -bb )
      o3 = math.exp( -cc )
      
      AA[i][j] = o1
      BB[i][j] = o2
      CC[i][j] = o3

for i in range(iterr): 
    print i   
    for j in range(No_Of_Users):
        #print j
        for k in range(100):
        
            val1 = np.zeros(shape=(1, latent_leng))
            val2 = np.zeros(shape=(1, latent_leng))
            val3 = np.zeros(shape=(1, latent_leng))
            val4 = np.zeros(shape=(1, latent_leng))
            val5 = np.zeros(shape=(1, latent_leng))

            transu = np.transpose(learnedu[j])                  # k*1
            transt = np.transpose(learnedt[k])                  # k*1 
            multip = np.matmul(learnedu[j], transt)             # 1*1
            xx = (matu_f[j][k] - multip)                        # 1*1
            
            val1 = (xx*learnedt[k])                             # 1*k
            val7 = (xx*learnedu[j])                             # 1*k 
            
            for ll in range(No_Of_Users):
                val2 += diff(j, ll)
                val3 += diff2(j, ll)
                val4 += diff3(j, ll)

            val2 = normalize(val2)
            val3 = normalize(val3)
            val4 = normalize(val4)

            val5 = (lambdau*learnedu[j])
            val8 = (lambdav*learnedt[k])
            
            learnedu[j] = learnedu[j] + (betau*(val1 - alphap*val2 - alphaq*val3 - alphar*val4 - val5))
            learnedt[k] = learnedt[k] + (betaw*(val7 - val8))
            
            learnedu[j] = normalize(learnedu[j])
            learnedt[k] = normalize(learnedt[k])  
        #print learnedu[j]

    #print 'Learnedu: ', learnedu 
    #print 'Learnedt: ', learnedt

labell = []
for i in range(No_Of_Users):
    for j in range(No_Of_Users):
       if(i!=j):
        simimat[i][j] = frob(i, j)
    maxxmat[i] = maxx(simimat[i])
    labell.append(i)

KK = 50
yx = zip(maxxmat, labell)
yx.sort(reverse=True)
anss = 0
ytrue = []
ypred = []
  
#print 'yx: ', yx
for i in range(len(yx)):
    if( i<KK ):
        ypred.append(1)
        if( yx[i][1] < cust_users ):
            anss += 1
            ytrue.append(1)
        else:
            ytrue.append(0)  
    else:
        ypred.append(0)
        if( yx[i][1] < cust_users ):
            ytrue.append(1)
        else:
            ytrue.append(0)

print( float(anss)/No_Of_Users )
print 'ypred ', ypred
print 'ytrue ', ytrue

print float(anss)/cust_users
fpr, tpr, thresholds = roc_curve(ytrue, ypred, pos_label=2)

print(f1_score(ytrue, ypred, average="macro"))
print(precision_score(ytrue, ypred, average="macro"))
print(recall_score(ytrue, ypred, average="macro"))    
print(roc_auc_score(ytrue, ypred, average="macro"))

print(f1_score(ytrue, ypred, average="micro"))
print(precision_score(ytrue, ypred, average="micro"))
print(recall_score(ytrue, ypred, average="micro"))    
print(roc_auc_score(ytrue, ypred, average="micro"))