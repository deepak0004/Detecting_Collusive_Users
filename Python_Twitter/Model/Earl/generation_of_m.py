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

all_data_of_checked_users = []
dictt = {}
total_topics = 100
no_top_words = 10
No_Of_Users = 100
#st = sys.argv[1]
#print st
#config = {}
#execfile(st, config)
matu_f = np.zeros(shape=(No_Of_Users, total_topics)) 

def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)
def display_topics2(model, feature_names, no_top_words):
    dictt2 = {}
    for topic_idx, topic in enumerate(model.components_):
        dictt2[topic_idx] = []
        for i in topic.argsort()[:-no_top_words - 1:-1]:
            dictt2[topic_idx].append(feature_names[i])
    return dictt2
def topiclda(X, no_topics, no_top_words):
    no_features = total_topics
    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    tf_vectorizer = CountVectorizer(max_df=1.0, min_df=1, max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(X)
    tf_feature_names = tf_vectorizer.get_feature_names()
    # Run LDA
    lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    oioi = display_topics2(lda, tf_feature_names, no_top_words)
    return oioi
def textobt(results):
    vall = []
    for status in results:
        status["text"] = unicodedata.normalize('NFKD', status["text"]).encode('ascii','ignore')
        vall.append( status["text"] )
    return vall

us_list = []
inputt = open('total_users.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

for username in us_list:
    username = username.strip() 
    username = username.strip('\n')
    username = username.split('/')
    username = username[3]
    
    print username

    results = []
    flag2 = 0
    while( flag2 == 0 ):
        results = []
        try:
            consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
            twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
            results = twitter.statuses.user_timeline(screen_name = username, count = 50)
            flag2 = 1
        except Exception as e:
            print e
            print 'yo3'
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
                    print 'waiting1'
                    time.sleep(60)
                    continue
            flag2 = 1  
    if( len(results)!=0 ):
        results = textobt(results)
        all_data_of_checked_users.extend(results)

no_features = total_topics
# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
tf_vectorizer = CountVectorizer(max_df=1.0, min_df=1, max_features=no_features, stop_words='english')
tf = tf_vectorizer.fit_transform(all_data_of_checked_users)
tf_feature_names = tf_vectorizer.get_feature_names()
no_topics = total_topics
# Run LDA
lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
for topic_idx, topic in enumerate(lda.components_):
    dictt[topic_idx] = []
    for i in topic.argsort()[:-no_top_words - 1:-1]:
        dictt[topic_idx].append(tf_feature_names[i])

print 'dictt[0]: ', dictt[0]
print 'dictt[1]: ', dictt[1]

with open('dictt.dump', "wb") as fp: 
    pickle.dump(dictt, fp)

coun = 0
for username in us_list:
        username = username.strip() 
        username = username.strip('\n')
        username = username.split('/')
        username = username[3]
        print username

        flag = 0
        while( flag == 0 ):
            query = []
            try:
                consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
                twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
                query = twitter.friends.ids(screen_name = username, count = 50)
                flag = 1
        
                for n in range(0, len(query["ids"])):
                    ids = query["ids"][n]

                    results = []
                    flag2 = 0
                    while( flag2 == 0 ):
                        try:
                            #print ids
                            consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
                            twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
                            results = twitter.statuses.user_timeline(user_id = ids, count = 100)
                            #print results
                            flag2 = 1
                        except Exception as e:
                            print e
                            print 'yo2'
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
                                    print 'waiting3'
                                    time.sleep(60)
                                    continue
                            flag2 = 1
                    
                    if( len(results)!=0 ):
                        results = textobt(results)
                        results.append('The world is great')
                        topmodelfri = topiclda(results, 5, 10)
                        #print 'Topic:::::: ', topmodelfri
                        for i in range(total_topics):
                            for k in range(5):
                                 flagx1 = jaccard_similarity(dictt[i], topmodelfri[k])
                                 #print 'dictt[i]: ', dictt[i]
                                 #print 'topmodelfri[k]: ', topmodelfri[k]
                                 #print 'flagx1: ', flagx1
                                 if( flagx1>=0.0001 ):
                                    #print 'yozzzzzzzzz'
                                    matu_f[coun][i] += 1  
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
                flag = 1
        coun += 1
        if( (coun%50)==0 ):
	      with open('matu_f.dump', "wb") as fp: 
    	       pickle.dump(matu_f, fp)
