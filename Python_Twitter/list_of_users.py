import pickle
import time
import sys
from Object import *
from twitter import *
import unicodedata
import json

st = sys.argv[1]
print st
config = {}
execfile(st, config)
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
userveri = []
usercust = []
us_list = []
dictt = {}

inputt = open('tweet_links.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

for username in us_list:
        username = username.strip() 
        username = username.strip('\n')
        username = username.split('/')
        username = username[3]
        print username
        usercust.append(username)
        dictt[username] = []

        flag = 0
        while( flag == 0 ):
            query = []
            try:
                query = twitter.friends.ids(screen_name = username, count = 2000)
                flag = 1
        
                for n in range(0, len(query["ids"]), 98):
                    ids = [-1]
                    ids.extend( query["ids"][n:n+98] )
                    ids.append(-1)

                    flag2 = 0
                    while( flag2 == 0 ):
                        try:
                            subquery = twitter.users.lookup(user_id = ids)
                            flag2 = 1
                            for user in subquery:
                            	 #print user["verified"]
                                 if( str(user["verified"])=="True" ):
                                    userveri.append( str(user["screen_name"]) )
                                 else:
                                    usercust.append( str(user["screen_name"]) )
                                 #dictt[username].append( str(user["screen_name"]) )
                        except Exception as e:
                            print e
                            print 'yo2'
                            time.sleep(60)

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
                print len(stst)  
                if( len(stst)>=4 ):
                    op =  stst[3][1] + stst[3][2]
                    print op
                    if( op == "88" ):
                        time.sleep(60)
                        continue
                flag = 1 

        flag = 0
        while( flag == 0 ):
            try:
                query = twitter.followers.ids(screen_name = username, count = 2000)
                flag = 1

                for n in range(0, len(query["ids"]), 98):
                    ids = [-1]
                    ids.extend( query["ids"][n:n+98] )
                    ids.append(-1)

                    flag2 = 0
                    while( flag2 == 0 ):
                        try:
                            subquery = twitter.users.lookup(user_id = ids)
                            flag2 = 1
                            for user in subquery:	
                            	 #print user["verified"] 
                                 if( str(user["verified"])=="True" ):
                                    userveri.append( str(user["screen_name"]) )
                                 else:
                                    usercust.append( str(user["screen_name"]) )
                                 #dictt[username].append( str(user["screen_name"]) )
                        except Exception as e:
                            print e
                            print 'yo4'
                            time.sleep(60)
            except TwitterError as e:
                print e
                print 'yo3'                
                stst = ''
                flag3 = 0
                for pp in e[0]:
                    if( pp=='{' or flag3 == 1 ):
                       stst += pp
                       flag3 = 1

                stst = stst.split(':')
                print len(stst)  
                if( len(stst)>=4 ):
	                op =  stst[3][1] + stst[3][2]
	                print op
	                if( op == "88" ):
	                    time.sleep(60)
	                    continue
                flag = 1
        print len(userveri), "    ", len(usercust)

with open("userveri.dump", "wb") as fp:  
    pickle.dump(userveri, fp)
    
with open("usercust.dump", "wb") as fp: 
    pickle.dump(usercust, fp)

#with open("dictt.dump", "wb") as fp: 
#    pickle.dump(dictt, fp)