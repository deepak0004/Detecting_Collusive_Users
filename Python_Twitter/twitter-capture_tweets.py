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
mapp_username_list = {}

inputt = open('user2_less_timeline.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

for username in us_list: 
        username = username.strip()
        username = username.strip('\n')
        #outputt.write(username + ",")
        flag = 0
        num = 1 
        while( flag == 0 ):
            try:
                print username, " ", len(username)
                results = twitter.statuses.user_timeline(screen_name = username, count = 200)
                flag = 1
                mapp_username_list[ username ] = []
                
                #-----------------------------------------------------------------------
                # loop through each of my statuses, and print its content
                #-----------------------------------------------------------------------
                for status in results:
                    status["text"] = unicodedata.normalize('NFKD', status["text"]).encode('ascii','ignore')
                    print num, " ", str(status["id"]), " ", status["text"], " ", str(status["favorite_count"]), " ", str(status["retweet_count"])
                    num += 1
                    #print 'boo2'
                    obj = Object(str(status["id"]), status["text"], str(status["favorite_count"]), str(status["retweet_count"]))        
                    #print 'boo'            
                    mapp_username_list[ username ].append( obj ) 
            except Exception:
                print 'yo', flag
                time.sleep(60)	

with open("user_and_who_retweeted.dump", "wb") as fp:   #Pickling
    pickle.dump(mapp_username_list, fp)