import pickle
import time
import sys
from Object import *
from twitter import *
import unicodedata
import json

st = sys.argv[1]
timeinterval = int(sys.argv[2])
print st
config = {}
execfile(st, config)
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

us_list = []
dictt = {}
dictt2 = {}
mapp_username_list = {}

inputt = open('tweet_links.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

tt = 2
while(tt>0):
    tt -= 1
    for username in us_list:
            username = username.strip() 
            username = username.strip('\n')
            username = username.split('/')
            username = username[3]
            print username
                           
            flag2 = 0
            while( flag2 == 0 ):
                inter = 0
                try:
                    queryy = twitter.followers.ids(screen_name = username, count = 100)
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

                mapp_username_list[ username ] = inter
    
    time.sleep(timeinterval)

with open('mapp_username_list.dump', "wb") as fp:
    pickle.dump(mapp_username_list, fp)