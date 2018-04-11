import pickle
import time
import sys
from Object import *
from twitter import *
import unicodedata
import json
import numpy as np

num = int(sys.argv[4])
lowerb = int(sys.argv[2])
upperb = int(sys.argv[3])
st = sys.argv[1]
print st
config = {}
execfile(st, config)
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
userveri = []
usercust = []
us_list = []
dictt = {}

with open("userveri.dump", "rb") as fp:   # Unpickling
    userveri = pickle.load(fp)

with open("usercust.dump", "rb") as fp:   # Unpickling
    usercust = pickle.load(fp)

userss = userveri
dictt = {}
userss.extend(usercust)
WW = np.zeros(shape=(6000, 6000)) 

usercust = usercust[:2000]
userveri = userveri[:4000]

coun = 0
for username in userss:
        coun += 1
        print coun
        if( coun<=lowerb ):
            continue
        if( coun>=upperb ):
            continue
        dictt[username] = []
        flag = 0
        while( flag == 0 ):
            query = []
            try:
                query = twitter.friends.ids(screen_name = username, count = 1000)
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
                            	 dictt[username].append( str(user["screen_name"]) )
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
                query = twitter.followers.ids(screen_name = username, count = 1000)
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
                                dictt[username].append( str(user["screen_name"]) )
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
                print stst  
                if( len(stst)>=4 ):
	                op =  stst[3][1] + stst[3][2]
	                print op
	                if( op == "88" ):
	                    time.sleep(60)
	                    continue
                flag = 1
        print len(userveri), "    ", len(usercust)

with open('dictt' + str(num) + '.dump', "wb") as fp: 
    pickle.dump(dictt, fp)