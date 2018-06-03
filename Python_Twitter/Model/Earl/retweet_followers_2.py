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
import api_settings

settings_file =  "apikeys/apikeys.txt"
history_file = "apikeys/api_history.txt"

dictt = {}
total_topics = 1000
no_top_words = 10

#st = sys.argv[1]
#print st
#config = {}
#execfile(st, config)
#twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

user_follower_list = {}
us_list = []
dictt_retweet_follo = {}
inputt = open('total_users.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

coun = 0
for username in us_list:
    coun += 1
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
            consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
            twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
            query = twitter.followers.ids(screen_name = username, count = 50)
            flag2 = 1 
            #coun = 0
            for n in range(0, len(query["ids"]), 200):
                ids = query["ids"][n:n+100]
                for j in range(len(ids)):
                    idsslist.append(ids[j])
                #coun += 1
                #if( coun>=30 ):
                #    break
            #print idsslist
        except TwitterError as e:
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
            flag2 = 1

    flag2 = 0
    while( flag2 == 0 ):
        try:
            consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
            twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
            results = twitter.statuses.user_timeline(screen_name = username, count = 100)
            flag2 = 1
        except TwitterError as e:
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
            flag2 = 1

    #print results
    if( len(results) ):
        oioip = 0
        for status in results:
            flag2 = 0
            while( flag2 == 0 ):
                try:
                    consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
                    twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
                    retweets = twitter.statuses.retweets._id(_id = status["id"])
                    for retweet in retweets:
                        strr =  (retweet["user"]["id"]) 
                        #print oioip
                        #oioip += 1
                        if( strr in idsslist ):
                            anss += 1
                    flag2 = 1
                except TwitterError as e:
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
                    flag2 = 1 
    
    leng = 1
    if( len(idsslist)!=0 ):
       leng = len(idsslist)                 
    anss = float(anss)/leng
    dictt_retweet_follo[username] = anss
    print 'dictt_retweet_follo: ', dictt_retweet_follo[username]
    print coun
    if( (coun%200)==0 ):
        with open('dictt_retweet_follo.dump', "wb") as fp:
            pickle.dump(dictt_retweet_follo, fp)        

with open('dictt_retweet_follo.dump', "wb") as fp:
    pickle.dump(dictt_retweet_follo, fp)
