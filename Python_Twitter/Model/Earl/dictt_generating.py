import pickle
import time
import sys
#from Object import *
from twitter import *
import unicodedata
import json
import numpy as np
import api_settings

settings_file =  "apikeys/apikeys.txt"
history_file = "apikeys/api_history.txt"
dictt = {}
us_list = []

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
        print username, " ", coun

        dictt[username] = []
        flag = 0
        while( flag == 0 ):
            query = []
            try:
                consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
                twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
                query = twitter.friends.ids(screen_name = username, count = 1000)
                flag = 1
                
                op2 = 0
                for n in range(0, len(query["ids"]), 98):
                    op2 += 1
                    if( op2>=30 ):
                       break  
                    ids = [-1]
                    ids.extend( query["ids"][n:n+98] )
                    ids.append(-1)

                    flag2 = 0
                    while( flag2 == 0 ):
                        try:
                            subquery = twitter.users.lookup(user_id = ids)
                            flag2 = 1
                            for user in subquery:
                            	 dictt[username].append( str(user["screen_name"]) )
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
			                print stst
			                if( len(stst)>=4 ):
			                    op =  stst[3][1] + stst[3][2]
			                    print op
			                    if( op == "88" ):
			                        time.sleep(60)
			                        continue
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
                print stst
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
                consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
                twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
                query = twitter.followers.ids(screen_name = username, count = 1000)
                flag = 1
                  
                op2 = 0  
                for n in range(0, len(query["ids"]), 98):
                    op2 += 1
                    if( op2>= 30 ):
                      break
                    ids = [-1]
                    ids.extend( query["ids"][n:n+98] )
                    ids.append(-1)

                    flag2 = 0
                    while( flag2 == 0 ):
                        try:
                            subquery = twitter.users.lookup(user_id = ids)
                            flag2 = 1
                            for user in subquery:	
                                dictt[username].append( str(user["screen_name"]) )
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
			                print stst
			                if( len(stst)>=4 ):
			                    op =  stst[3][1] + stst[3][2]
			                    print op
			                    if( op == "88" ):
			                        time.sleep(60)
			                        continue
			                flag2 = 1 

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
                print stst  
                if( len(stst)>=4 ):
	                op =  stst[3][1] + stst[3][2]
	                print op
	                if( op == "88" ):
	                    time.sleep(60)
	                    continue
                flag = 1
        #print len(userveri), "    ", len(usercust)

with open('dictt.dump', "wb") as fp: 
    pickle.dump(dictt, fp)
