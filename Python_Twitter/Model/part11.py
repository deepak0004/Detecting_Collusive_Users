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
while(tt<3):
    tt += 1
    for username in us_list:
            username = username.strip() 
            username = username.strip('\n')
            username = username.split('/')
            username = username[3]
            print username
            mapp_username_list[ username ] = 0
                           
            flag2 = 0
            while( flag2 == 0 ):
                pp = 100
                inter = []
                try:
                    consumer_key, consumer_secret, access_key, access_secret = api_settings.populate_Settings(settings_file, history_file)
                    twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
                    queryy = twitter.friends.ids(screen_name = username, count=100)
                    pp = min(pp, len(queryy)) 
                    flag2 = 1
                    #print 'bhaibhai'
                    if( username in dictt2 ):
                        prev_list = dictt2[ username ]
                    else:
                        prev_list = []
                    #print queryy
                    inter = set(queryy).intersection(set(prev_list))
                    dictt2[ username ] = queryy
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
                    flag2 = 1 

                mapp_username_list[ username ] = len(inter)/float(pp) 
                print mapp_username_list[ username ]
                if( tt and username not in mapp_username_list2 ):
                    mapp_username_list2[ username ] = mapp_username_list[ username ]
                elif(tt):
                    mapp_username_list2[ username ] = min(mapp_username_list2[ username ], mapp_username_list[ username ])
    
    with open('mapp_username_list2.dump', "wb") as fp:
        pickle.dump(mapp_username_list2, fp)
    with open('mapp_username_list2.dump', "wb") as fp:
        pickle.dump(mapp_username_list2, fp)

    time.sleep(timeinterval)
