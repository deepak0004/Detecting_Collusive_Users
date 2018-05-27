import pickle
import time
import sys
from Object import *
from twitter import *
import unicodedata
import json
from sklearn.svm import LinearSVR
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix, roc_curve, roc_auc_score, auc
import api_settings
import numpy as np
from sklearn import svm

settings_file =  "apikeys/apikeys.txt"
history_file = "apikeys/api_history.txt"

#st = sys.argv[1]
#timeinterval = int(sys.argv[2])
#print st
#config = {}
#execfile(st, config)
#twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

noofusers = 1000
cust = 300
features = []
labelss = []
us_list = []
dictt = {}
mapp_username_list = {}
nooffeatures = 11
star = 151
endd = 450
rows = 0
'''
noofusers = 10
star = 3
endd = 7
cust = 5
'''
inputt = open('total_users.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

#listt = [-1]
outputt = open('full_users.txt', 'w', 0)
coun = 0
for username in us_list:
        username = username.strip() 
        username = username.strip('\n')
        username = username.split('/')
        username = username[3]
        coun += 1

        flag = 0
        while( flag == 0 ):
            try:
                #print 'io'
                print username
                consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
                twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
                query = twitter.users.lookup( screen_name=username ) 
                #print 'po'
                flag = 1
                noofurl = 0
                retweet = 0
                prev_list = []
                inter = 0
                tweet = 0
                yocheck = 0

                for user in query:
                        #print user["screen_name"]
                        flag2 = 0
                        while( flag2 == 0 ):
                            try:
                                consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
                                twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
                                results = twitter.statuses.user_timeline(screen_name = user["screen_name"], count = 100)
                                flag2 = 1
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
                                flag2 = 1                 
                        
                        hashh = 0
                        leng = 0
                        mention = 0
                        spamm = 0
                        #print results
                        for status in results:
                            #print status["text"]
                            #status["text"] = unicodedata.normalize('NFKD', status["text"]).encode('ascii','ignore')
                            obj = Object(str(status["id"]), status["text"], str(status["favorite_count"]), str(status["retweet_count"]))
                            #print 'reached here1'
                            if( username in mapp_username_list ):
                               mapp_username_list[ username ].append( obj ) 
                            else:
                               mapp_username_list[ username ] = [obj]
                            if( ("http" in status["text"]) or ("www." in status["text"]) ):
                               noofurl += 1
                            #print 'reached here2'
                            #print 'status retweet: ', status["retweeted"]
                            if( "True" in str(status["retweeted"]) ):
                               retweet += 1
                            else:
                               tweet += 1 

                            if( "#" in status["text"] ):
                               hashh += 1
                            if( "@" in status["text"] ):
                               mention += 1
                            leng = len(status["text"])
                            if( "free" in status["text"] or "click" in status["text"] or "deal" in status["text"] or "membership" in status["text"]):
                                spamm += 1


                        if( tweet>0 ):
                            tweet_retweet = "%.10f" % ( float(retweet) / tweet )
                        else:
                            tweet_retweet = 0 

                        fri = user["friends_count"]
                        foll = user["followers_count"] 
                        ratio =  "%.10f" %  ( float(foll) / (fri + foll) )
                        #print 'reached here 3'
                        print str(user["friends_count"]) + "," + str(user["followers_count"]) + ",", 
                        #print 'reached here 4'
                        print str(ratio) + "," + str(user["favourites_count"]) + ",",
                        print str(user["statuses_count"]) + "," + str(user["verified"]), ",",
                        print str(noofurl) + "," + str(retweet)

                        features.extend([float(user["friends_count"]), float(user["followers_count"]), float(ratio), float(user["favourites_count"]), float(user["statuses_count"]), float(noofurl), float(retweet), float(hashh), float(leng), float(mention), float(spamm)])
                        if( coun<=cust ):
                            labelss.append(1)
                        else:
                            labelss.append(0)
                        rows += 1
                        coun += 1
                        outputt.write(str(user["friends_count"]) + "," + str(user["followers_count"]) + "," + str(ratio) + "," + str(user["favourites_count"]) + "," + str(user["statuses_count"]) + "," + str(noofurl) + "," + str(retweet) + "\n")
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
                if( op == "17" ):
                    flag = 1
                    outputt.write("-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "\n")

trainvector = np.reshape( features, (rows, 11) )
trainlabel = np.reshape( labelss, (len(labelss), 1) )

with open('trainvector.dump', "wb") as fp:
    pickle.dump(trainvector, fp)

#print trainlabel

print('Defining')
#clf2 = KNeighborsClassifier(n_neighbors=5) 
#clf2 = GaussianNB()
clf2 = svm.LinearSVC()   # 0.554045444893
#clf2 = DecisionTreeClassifier(criterion = "gini")
#clf2 = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1) # 0.554045444893
print('Training')
clf2.fit(trainvector, trainlabel)
print 'Done'

ytrue = []
ypred = []
rejected = 0

for i in range(star, endd):
    if( i<cust ):
        ytrue.append(1)
    else:
        ytrue.append(0)
    op = trainvector[i] 
    ans = 0
    try:
        #print op
        labell = clf2.predict([op])
        ypred.append(labell)
        if( labell==1 and i<=cust ):
            ans += 1
        elif( labell==0 and i>cust ):
            ans += 1 
    except Exception: 
        rejected += 1
        pass

print 'ypred ', ypred
print 'ytrue ', ytrue

print float(ans)/cust
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

#with open('trainvector.dump', "wb") as fp:
#    pickle.dump(trainvector, fp)