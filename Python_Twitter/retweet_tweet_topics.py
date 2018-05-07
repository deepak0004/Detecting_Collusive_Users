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
total_topics = 20
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
def diff(i, j):
   o1 = learnedu[i]
   o2 = learnedu[j]
   subb = o1 - o2
   subb = (alphac[i][j]*subb)
   return subb
def diff2(i, j):
   o1 = learnedu[i]
   o2 = learnedu[j]
   subb = o1 - o2
   subb = (alphag[i][j]*subb)
   return subb
def frob(i, j):
   o1 = learnedu[i]
   o2 = learnedu[j]
   anss = 0
   for p in range(latent_leng):
       anss += abs( float(o1[p] - o2[p])*(o1[p] - o2[p]) )
   anss = (1.0/(1+anss))
   return anss
def maxx(vect):
   ko = 0
   for j in range(len(vect)):
      ko = max(ko, vect[j])
   return ko
def textobt(results):
    vall = []
    for status in results:
        status["text"] = unicodedata.normalize('NFKD', status["text"]).encode('ascii','ignore')
        vall.append( status["text"] )
    return vall

retweet_tweet_dictt = {}
us_list = []
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
    retweet_tweet_dictt[ username ] = 0
    results = []
    flag2 = 0
    while( flag2 == 0 ):
        results = []
        try:
            results = twitter.statuses.user_timeline(screen_name = username, count = 100)
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

    tweets_listt = []
    if( len(results)==0 ):
        continue

    results = textobt(results)
    results.append('The world is great')
    topmodeltweet = topiclda(results, 5, 10)

    no_features = total_topics
    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    tf_vectorizer = CountVectorizer(max_df=1.0, min_df=1, max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(results)
    tf_feature_names = tf_vectorizer.get_feature_names()
    no_topics = total_topics

    # Run LDA
    lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    for topic_idx, topic in enumerate(lda.components_):
        dictt[topic_idx] = []
        for i in topic.argsort()[:-no_top_words - 1:-1]:
            tweets_listt.append(tf_feature_names[i])

    flag2 = 0
    while( flag2 == 0 ):
        query = []
        try:
            query = twitter.followers.ids(screen_name = username, count = 100)
            flag2 = 1
    
            for n in range(0, len(query["ids"])):
                ids = query["ids"][n]

                results = []
                flag2 = 0
                while( flag2 == 0 ):
                    try:
                        results = twitter.statuses.user_timeline(user_id = ids, count = 100)
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
                                print 'waiting2'
                                time.sleep(60)
                                continue
                        flag2 = 1
                
                if( len(results)==0 ):
                    continue

                results = textobt(results)
                results.append('The world is great')
                topmodelfri = topiclda(results, 5, 10)
                
                for i in range(5):
                    for k in range(5):
                         flagx1 = jaccard_similarity(topmodeltweet[i], topmodelfri[k])
                         retweet_tweet_dictt[ username ] += flagx1 

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
                    print 'waiting3'
                    time.sleep(60)
                    continue
            flag2 = 1

with open('retweet_tweet_dictt.dump', "wb") as fp:
    pickle.dump(retweet_tweet_dictt, fp)