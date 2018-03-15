import pickle
import time
import sys
from Object import *
from twitter import *
import unicodedata

st = sys.argv[1]
print st
config = {}
execfile(st, config)
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

us_list = []
dictt = {}
mapp_username_list = {}

inputt = open('tweet_links.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

#listt = [-1]
outputt = open('plotting_data.txt', 'w', 0)
for username in us_list:
        username = username.strip() 
        username = username.strip('\n')
        username = username.split('/')
        username = username[3]
        #print username
        #listt.append(username)

        #if( ( len(listt)%4 ) == 0 ):
        #    listt.append(-1)
        #    print listt
            #outputt.write(username + ",")
        flag = 0
        while( flag == 0 ):
            try:
                #print 'io'
                #print username
                query = twitter.users.lookup( screen_name=username ) 
                #print 'po'
                flag = 1
                noofurl = 0
                retweet = 0

                for user in query:
                        print user["screen_name"]
                        flag2 = 0
                        while( flag2 == 0 ):
                            try:
                                results = twitter.statuses.user_timeline(screen_name = user["screen_name"], count = 20)
                                flag2 = 1
                            except Exception:
                                print 'yo2', " ", flag2
                                time.sleep(60) 
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
                            retweet += int(status["retweet_count"])

                        fri = user["friends_count"]
                        foll = user["followers_count"] 
                        ratio =  "%.10f" %  ( float(foll) / (fri + foll) )
                        
                        #print 'reached here 3'
                        print str(user["friends_count"]) + "," + str(user["followers_count"]) + ",", 
                        #print 'reached here 4'
                        print str(ratio) + "," + str(user["favourites_count"]) + ",",
                        print str(user["statuses_count"]) + "," + str(user["verified"]), ",",
                        print str(noofurl) + "," + str(retweet)

                        outputt.write(str(user["friends_count"]) + "," + str(user["followers_count"]) + "," + str(ratio) + "," + str(user["favourites_count"]) + "," + str(user["statuses_count"]) + "," + str(user["verified"]) + "," + str(noofurl) + "," + str(retweet) + "\n")
            except TwitterHTTPError as e:
                print '###########################################################'
                print '###########################################################'
                print '###########################################################'
                print '###########################################################'
                print e
                print '###########################################################'
                print '###########################################################'
                print '###########################################################'
                print '###########################################################'
                print e.message
                print '###########################################################'
                print '###########################################################'
                print '###########################################################'
                print '###########################################################'             
                print 'yo', " ", flag
                time.sleep(60)

'''
if( len(listt)>1 ):
    listt.append(-1)
    #outputt.write(username + ",")
    flag = 0
    while( flag == 0 ):
        try:
            query = twitter.users.lookup(screen_name = listt) 
            flag = 1
            noofurl = 0
            retweet = 0

            for user in query:
                    flag2 = 0
                    while( flag2 == 0 ):
                        try:
                            results = twitter.statuses.user_timeline(screen_name = user["screen_name"], count = 20)
                            flag2 = 1
                        except Exception:
                            print 'yo2', " ", flag2
                            time.sleep(60) 

                    for status in results:
                        status["text"] = unicodedata.normalize('NFKD', status["text"]).encode('ascii','ignore')
                        obj = Object(str(status["id"]), status["text"], str(status["favorite_count"]), str(status["retweet_count"]))
                        mapp_username_list[ username ].append( obj ) 
                        if( ("http" in status["text"]) or ("www." in status["text"]) ):
                           noofurl += 1
                        retweet += int(status["retweet_count"])

                    fri = user["friends_count"]
                    foll = user["followers_count"] 
                    ratio =  "%.10f" %  ( float(foll) / (fri + foll) )
             
                    print user["friends_count"] + "," + user["followers_count"] + ",", 
                    print ratio + "," + user["favourites_count"] + ",",
                    print user["statuses_count"] + "," + user["verified"], ",",
                    print noofurl + "," + retweet
        except Exception:
            print 'yo', " ", flag
            time.sleep(60)
'''

with open("user_and_who_retweeted.dump", "wb") as fp:   #Pickling
    pickle.dump(mapp_username_list, fp)