import pickle
import time
import sys
from Object import *
from twitter import *
import unicodedata
import json
from sklearn.svm import LinearSVR
from sklearn.metrics import f1_score
import api_settings

settings_file =  "apikeys/apikeys.txt"
history_file = "apikeys/api_history.txt"

#st = sys.argv[1]
#timeinterval = int(sys.argv[2])
#print st
#config = {}
#execfile(st, config)
#twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

cust = 300
features = []
labelss = []
us_list = []
dictt = {}
mapp_username_list = {}
nooffeatures = 8

inputt = open('total_users.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

#listt = [-1]
outputt = open('full_users.txt', 'w', 0)
coun = 0
while(1):
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

                            #print results
                            for status in results:
                                #print status["text"]
                                status["text"] = unicodedata.normalize('NFKD', status["text"]).encode('ascii','ignore')
                                obj = Object(str(status["id"]), status["text"], str(status["favorite_count"]), str(status["retweet_count"]))
                                #print 'reached here1'
                                if( username in mapp_username_list ):
                                   mapp_username_list[ username ].append( obj ) 
                                else:
                                   mapp_username_list[ username ] = [obj]
                                if( ("http" in status["text"]) or ("www." in status["text"]) ):
                                   noofurl += 1
                                #print 'reached here2'
                                if( int(status["retweeted"])==1 ):
                                   retweet += 1
                                else:
                                   tweet += 1 

                            fri = user["friends_count"]
                            foll = user["followers_count"] 
                            ratio =  "%.10f" %  ( float(foll) / (fri + foll) )
                            #print 'reached here 3'
                            print str(user["friends_count"]) + "," + str(user["followers_count"]) + ",", 
                            #print 'reached here 4'
                            print str(ratio) + "," + str(user["favourites_count"]) + ",",
                            print str(user["statuses_count"]) + "," + str(user["verified"]), ",",
                            print str(noofurl) + "," + str(retweet)

                            features.extend([float(user["friends_count"]), float(user["followers_count"]), float(ratio), float(user["favourites_count"]), float(user["statuses_count"]), float(user["verified"]), float(noofurl), float(retweet)])
                            if( coun<=cust ):
                                labelss.append(1)
                            else:
                                labelss.append(0)
                            outputt.write(str(user["friends_count"]) + "," + str(user["followers_count"]) + "," + str(ratio) + "," + str(user["favourites_count"]) + "," + str(user["statuses_count"]) + "," + str(user["verified"]) + "," + str(noofurl) + "," + str(retweet) + "\n")
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

trainvector = np.reshape( features, (len(features), 11) )
trainlabel = np.reshape( labelss, (len(labelss), 1) )

print('Defining')
#clf2 = KNeighborsClassifier(n_neighbors=5) 
#clf2 = GaussianNB()
clf2 = svm.LinearSVC()   # 0.554045444893
#clf2 = DecisionTreeClassifier(criterion = "gini")
#clf2 = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1) # 0.554045444893
print('Training')
clf2.fit(trainvector, trainlabel)

for i in range(151, 450):
    op = features[i] 
    ans = 0
    try:
        labell = clf2.predict([op])
        if( labell==1 and i<=300 ):
            ans += 1
        elif( labell==0 and i>300 ):
            ans += 1 
    except Exception: 
        rejected += 1
        pass

print ans/300.0

with open('trainvector.dump', "wb") as fp:
    pickle.dump(trainvector, fp)