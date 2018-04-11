import pickle
import time
import sys
import numpy as np
from twitter import *
import unicodedata
import json
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation
from scipy.spatial.distance import cdist
from scipy.spatial import distance

dictt = {}
No_Of_Users = 10
total_topics = 100
def display_topics(model, feature_names, no_top_words):
    global dictt
    for topic_idx, topic in enumerate(model.components_):
        dictt[topic_idx] = []
        for i in topic.argsort()[:-no_top_words - 1:-1]:
            dictt[topic_idx].append(feature_names[i])
        print '##########', topic_idx, '##########'
def display_topics2(model, feature_names, no_top_words):
    oioi = []
    for topic_idx, topic in enumerate(model.components_):
        for i in topic.argsort()[:-no_top_words - 1:-1]:
            oioi.append(feature_names[i])
    return oioi
def topiclda(X, no_topics, no_top_words):
    no_features = 1000
    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    tf_vectorizer = CountVectorizer(max_df=2, min_df=1, max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(X)
    tf_feature_names = tf_vectorizer.get_feature_names()
    # Run LDA
    lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    oioi = display_topics2(lda, tf_feature_names, no_top_words)
    return oioi
def intersec(li1, li2):
    for i1 in li1:
        for j1 in li2:
            if( i1==j1 ):
                return 1
    return 0
def textobt(results):
    vall = []
    for status in results:
        status["text"] = unicodedata.normalize('NFKD', status["text"]).encode('ascii','ignore')
        vall.append( status["text"] )
    return vall

mat1 = np.zeros(shape=(total_topics, total_topics)) 
mat2 = np.zeros(shape=(total_topics, total_topics)) 
st = sys.argv[1]
print st
config = {}
execfile(st, config)
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
userveri = []
usercust = []
us_list = []
dictt = {}
coun = 0

inputt = open('tweet_links.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

all_data_of_checked_users = []
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
                    time.sleep(60)
                    continue
            flag2 = 1  
    if( len(results)!=0 ):
        results = textobt(results)
        all_data_of_checked_users.extend(results)

#print '############################################################'
#print all_data_of_checked_users
#print '############################################################'
no_features = 1000
# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
tf_vectorizer = CountVectorizer(max_df=2, min_df=1, max_features=no_features, stop_words='english')
tf = tf_vectorizer.fit_transform(all_data_of_checked_users)
tf_feature_names = tf_vectorizer.get_feature_names()
no_topics = total_topics
# Run LDA
lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
no_top_words = 10
display_topics(lda, tf_feature_names, no_top_words)

for username in us_list:
        username = username.strip() 
        username = username.strip('\n')
        username = username.split('/')
        username = username[3]
        print username

        flag = 0
        while( flag == 0 ):
            results = []
            try:
                results = twitter.statuses.user_timeline(screen_name = username, count = 100)
                flag = 1        
            except Exception as e:
                print e
                print 'yo4'
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
        #print 'len(results): ', len(results)
        if( len(results)==0 ):
            continue
        results = textobt(results)
        topicmodeluser = topiclda(results, 1, 10)
        #print topicmodeluser
        flag = 0
        while( flag == 0 ):
            query = []
            try:
                query = twitter.friends.ids(screen_name = username, count = 100)
                flag = 1
        
                for n in range(0, len(query["ids"])):
                    ids = query["ids"][n]

                    results = []
                    flag2 = 0
                    while( flag2 == 0 ):
                        try:
                            #print ids
                            results = twitter.statuses.user_timeline(user_id = ids, count = 100)
                            #	print results
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
                                    time.sleep(60)
                                    continue
                            flag2 = 1
                    
                    if( len(results)!=0 ):
              	        results = textobt(results)
                        topmodelfri = topiclda(results, 1, 10)
                        print 'Topic:::::: ', topmodelfri
                        if( coun<No_Of_Users ):
                            for i in range(total_topics):
                              for j in range(total_topics):
                                 flagx1 = intersec(dictt[i], topicmodeluser)
                                 flagx2 = intersec(dictt[j], topmodelfri)
                                 if( flagx1==1 and flagx2==1 ):
                                    print 'yozzzzzzzzz'
                                    mat1[i][j] += (1/100.0)
                        else:
                            for i in range(total_topics):
                              for j in range(total_topics):
                                 flagx1 = intersec(dictt[i], topicmodeluser)
                                 flagx2 = intersec(dictt[j], topmodelfri)
                                 if( flagx1==1 and flagx2==1 ):
                                    print 'yozzzzzzzzz'
                                    mat2[i][j] += (1/100.0)

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

with open('mat1.dump', "wb") as fp: 
    pickle.dump(mat1, fp)
with open('mat2.dump', "wb") as fp: 
    pickle.dump(mat2, fp)

mat1 = np.reshape(mat1, (1, total_topics*total_topics))
mat2 = np.reshape(mat2, (1, total_topics*total_topics))
dst = distance.euclidean(mat1, mat2)
print dst