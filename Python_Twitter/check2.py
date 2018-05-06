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

all_data_of_checked_users = []
dictt = {}
No_Of_Users = 20
cust_users = 10
total_topics = 1000
latent_leng = 10
iterr = 100
betau = 0.4
betat = 0.4
lambdau = 0.4
lambdav = 0.4
no_top_words = 10

user_friratio = {}
user_tweet = {}
matu_f = np.zeros(shape=(No_Of_Users, total_topics)) 
matu_t = np.zeros(shape=(No_Of_Users, total_topics)) 
alphac = np.zeros(shape=(No_Of_Users, No_Of_Users))
alphag = np.zeros(shape=(No_Of_Users, No_Of_Users))
simimat = np.zeros(shape=(No_Of_Users, No_Of_Users))
maxxmat = np.zeros(shape=(No_Of_Users, 1))
learnedu = np.random.rand(No_Of_Users, latent_leng) 
learnedt = np.random.rand(total_topics, latent_leng) 

st = sys.argv[1]
print st
config = {}
execfile(st, config)
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

user_follower_list = {}
us_list = []
dictt_retweet_follo = {}
inputt = open('tweet_links2.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

for username in us_list:
    username = username.strip() 
    username = username.strip('\n')
    username = username.split('/')
    username = username[3]
    
    print username

    dictt_retweet_follo[username] = 0
    idsslist = []
    anss = 0

    flag2 = 0
    while( flag2 == 0 ):
        query = []
        try:
            query = twitter.followers.ids(screen_name = username, count = 100)
            flag2 = 1 
            coun = 0
            for n in range(0, len(query["ids"]), 100):
                ids = query["ids"][n:n+100]
                for j in range(len(ids)):
                    idsslist.append(ids[j])
                coun += 1
                if( coun>=30 ):
                    break
            print idsslist
        except TwitterError as e:
            print e
            stst = ''
            flag3 = 0
            for pp in e[0]:
                if( pp=='{' or flag3 == 1 ):
                   stst += pp
                   flag3 = 1

            stst = stst.split(':')
            op =  stst[3][1] + stst[3][2]
            print op
            if( op == "88" ):
                flag2 = 1
                continue
            print 'yo', " ", flag
            time.sleep(60)

    flag2 = 0
    while( flag2 == 0 ):
        try:
            results = twitter.statuses.user_timeline(screen_name = username, count = 100)
            flag2 = 1
        except TwitterError as e:
            print e
            stst = ''
            flag3 = 0
            for pp in e[0]:
                if( pp=='{' or flag3 == 1 ):
                   stst += pp
                   flag3 = 1

            stst = stst.split(':')
            op =  stst[3][1] + stst[3][2]
            print op
            if( op == "88" ):
                flag2 = 1
                continue
            print 'yo', " ", flag
            time.sleep(60)

    #print results
    oioip = 0
    for status in results:
        flag2 = 0
        while( flag2 == 0 ):
            try:
                retweets = twitter.statuses.retweets._id(_id = status["id"])
                for retweet in retweets:
                    strr =  (retweet["user"]["id"]) 
                    print oioip
                    oioip += 1
                    if( strr in idsslist ):
                        anss += 1
                flag2 = 1
            except TwitterError as e:
                print e
                stst = ''
                flag3 = 0
                for pp in e[0]:
                    if( pp=='{' or flag3 == 1 ):
                       stst += pp
                       flag3 = 1

                stst = stst.split(':')
                op =  stst[3][1] + stst[3][2]
                print op
                if( op == "88" ):
                    flag2 = 1
                    continue
                print 'yo', " ", flag
                time.sleep(60)
   
    anss = float(anss)/100
    print anss

    dictt_retweet_follo[username] = anss