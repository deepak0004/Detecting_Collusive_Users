import pickle
import time
import sys
from Object import *
from twitter import *
import unicodedata
import json
import api_settings

settings_file =  "apikeys/apikeys.txt"
history_file = "apikeys/api_history.txt"

#st = sys.argv[1]
timeinterval = int(sys.argv[1])
#print st
#config = {}
#execfile(st, config)

us_list = []
dictt = {}
dictt2 = {}
mapp_username_list = {}
mapp_username_list2 = {}

inputt = open('total_users.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

tt = 0
while(tt<5):
    for username in us_list:
            username = username.strip() 
            username = username.strip('\n')
            username = username.split('/')
            username = username[3]
            print username
            mapp_username_list[ username ] = 0
                           
            flag2 = 0
            while( flag2 == 0 ):
                pp = 100.0
                inter = []
                try:
                    consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
                    twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
                    queryy = twitter.friends.ids(screen_name = username, count=100)
                    #print queryy
                    pp = min(pp, len(queryy["ids"])) 
                    pp = max(pp, 1) 
                    flag2 = 1
                    #print 'bhaibhai'
                    if( username in dictt2 ):
                        prev_list = dictt2[ username ]
                    else:
                        prev_list = []
                    #print queryy
                    inter = set(queryy["ids"]).intersection(set(prev_list))
                    dictt2[ username ] = queryy["ids"]
                    #print inter 
                except TwitterError as e:
                    print e
                    print 'yo1'
                    stst = ''
                    flag3 = 0
                    for pp2 in e[0]:
                        if( pp2=='{' or flag3 == 1 ):
                           stst += pp2
                           flag3 = 1

                    stst = stst.split(':')
                    if( len(stst)>=4 ):
                        op =  stst[3][1] + stst[3][2]
                        print op
                        if( op == "88" ):
                            time.sleep(60)
                            continue
                    flag2 = 1 
                print pp 
                mapp_username_list[ username ] = len(inter)/float(pp) 
                print mapp_username_list[ username ]
                #if( username in mapp_username_list2 ):
                #    print 'boooooooo' 
                #print len(mapp_username_list2)
                if( (tt) and (username not in mapp_username_list2) ):
                    mapp_username_list2[ username ] = mapp_username_list[ username ]
                elif(tt):
                    #print 'yo'
                    mapp_username_list2[ username ] = min(mapp_username_list2[ username ], mapp_username_list[ username ])
                    print mapp_username_list2[ username ]

    
    with open('mapp_username_list2' + str(tt)  + '.dump', "wb") as fp:
        pickle.dump(mapp_username_list2, fp)
    tt += 1

    time.sleep(timeinterval)
