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
alphak = np.zeros(shape=(No_Of_Users, No_Of_Users))
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
def diff3(i, j):
   o1 = learnedu[i]
   o2 = learnedu[j]
   subb = o1 - o2
   subb = (alphak[i][j]*subb)
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

coun = 0
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
                        print 'waiting2'
                        time.sleep(60)
                        continue
                flag = 1
        #print 'len(results): ', len(results)
        if( len(results)==0 ):
            continue
        results = textobt(results)
        results.append('The world is great')
        topicmodeluser = topiclda(results, 5, 10)
        #print 'Topic:::::: ', topicmodeluser
        for i in range(total_topics):
            for k in range(5):
                 flagx1 = jaccard_similarity(dictt[i], topicmodeluser[k])
                 #print 'dictt[i]: ', dictt[i]
                 #print 'topmodelfri[k]: ', topmodelfri[k]
                 #print 'flagx1: ', flagx1
                 if( flagx1>=0.0001 ):
                    #print 'yozzzzzzzzz'
                    matu_t[coun][i] += 1  
        flag = 0
        while( flag == 0 ):
            query = []
            try:
                query = twitter.followers.ids(screen_name = username, count = 100)
                flag = 1
        
                for n in range(0, len(query["ids"])):
                    ids = query["ids"][n]

                    results = []
                    flag2 = 0
                    while( flag2 == 0 ):
                        try:
                            #print ids
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

with open('matu_t.dump', "wb") as fp: 
    pickle.dump(matu_t, fp)
with open('matu_f.dump', "wb") as fp: 
    pickle.dump(matu_t, fp)
with open("retweet_tweet_dictt.dump", "rb") as fp:  
    retweet_tweet_dictt = pickle.load(fp)
with open("mapp_username_list.dump", "rb") as fp:  
    mapp_username_list = pickle.load(fp)
with open("dictt_retweet_follo.dump", "rb") as fp:  
    dictt_retweet_follo = pickle.load(fp)

for i in range(No_Of_Users):
    for j in range(No_Of_Users):
      o1 = retweet_tweet_dictt[i]
      o2 = retweet_tweet_dictt[j]
      o3 = mapp_username_list[i]
      o4 = mapp_username_list[j]
      o5 = dictt_retweet_follo[i]
      o6 = dictt_retweet_follo[j]

      aa = 1.0 - min(o1, o2)
      bb = 1.0 - min(o3, o4)
      cc = max(o5, o6)

      o1 = 1.0 - math.exp( -aa )
      o2 = 1.0 - math.exp( -bb )
      o3 = math.exp( -cc )
      
      alphac[i][j] = o1
      alphag[i][j] = o2
      alphak[i][j] = o3

with open('alphac.dump', "wb") as fp: 
    pickle.dump(alphac, fp)
with open('alphag.dump', "wb") as fp: 
    pickle.dump(alphag, fp)
with open('alphak.dump', "wb") as fp: 
    pickle.dump(alphak, fp)

for i in range(iterr):    
    user_mat = np.zeros(shape=(No_Of_Users, latent_leng))
    user_mat2 = np.zeros(shape=(No_Of_Users, latent_leng))
    user_mat3 = np.zeros(shape=(No_Of_Users, latent_leng))

    for j in range(No_Of_Users):
        for k in range(j+1, No_Of_Users):
            user_mat[j] += diff(j, k)
            user_mat2[j] += diff2(j, k)
            user_mat3[j] += diff3(j, k)

    transu = np.transpose(learnedu)
    transt = np.transpose(learnedt)
  
    multip = np.matmul(learnedu, transt)          # U*T
    valuee = matu_f - multip                      # U*T     
    firstterm = np.matmul(valuee, learnedt)       # U*k      
    secondterm = user_mat[j]
    thirdterm = user_mat2[j]
    onemore = user_mat3[j]
    fourthterm = (lambdau * learnedu)
    valueetrans = np.transpose(valuee)
    fifthterm = np.matmul(valueetrans, learnedu)  # T*k
    sixthterm = (lambdav * learnedt)

    valuee2 = matu_t - multip                     # U*T
    extraau = np.matmul(valuee2, learnedt)   
    valueetrans2 = np.transpose(valuee2)
    extraav = np.matmul(valueetrans2, learnedu)

    learnedu = learnedu + ( betau * ( extraau + firstterm - secondterm - thirdterm - onemore - fourthterm ) )
    learnedt = learnedt + ( betat * ( extraav + fifthterm - sixthterm - onemore) )

labell = []
for i in range(No_Of_Users):
    for j in range(No_Of_Users):
        simimat[i][j] = frob(j, k)
    maxxmat[i] = maxx(simimat[i])
    labell.append(i)

with open('maxxmat.dump', "wb") as fp: 
    pickle.dump(maxxmat, fp)

yx = zip(maxxmat, labell)
yx.sort(reverse=True)
anss = 0
#print yx

for i in range(len(yx)):
    if( i<10 ):
        #print yx[i][1]
        if( yx[i][1] < cust_users ):
            anss += 1

print( float(anss)/50.0 )