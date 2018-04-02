import pickle
import time
import sys
from Object import *
from twitter import *
import unicodedata
import json

def edit_distance(s1, s2):
    m=len(s1)+1
    n=len(s2)+1

    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

    return tbl[i,j]

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

#listt = [-1]
outputt = open('plotting_data.txt', 'w', 0)

while(1):
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
                    print username
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
                            print user["screen_name"]
                            flag2 = 0
                            while( flag2 == 0 ):
                                try:
                                    results = twitter.statuses.user_timeline(screen_name = user["screen_name"], count = 200)
                                    flag2 = 1
                                except Exception as e:
                                    stst = ''
                                    flag3 = 0
                                    for pp in e[0]:
                                        if( pp=='{' or flag3 == 1 ):
                                           stst += pp
                                           flag3 = 1

                                    stst = stst.split(':')
                                    op =  stst[2]
                                    op = str(op)
                                    if( "Not authorized." in op ):
                                        flag2 = 1
                                        yocheck = 1
                                        outputt.write("-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "\n")
                                        continue
                                    print 'yo2', " ", flag2
                                    time.sleep(60)  
                            
                            if( yocheck==1 ):
                                continue                             

                            flag2 = 0
                            while( flag2 == 0 ):
                                try:
                                    queryy = twitter.friends.ids(screen_name = user["screen_name"], count = 5000)
                                    flag2 = 1
                                    #print 'bhaibhai'
                                    if( user["screen_name"] in dictt2 ):
                                        prev_list = dictt2[ user["screen_name"] ]
                                    else:
                                        prev_list = []
                                    #print queryy
                                    inter = set(queryy).intersection(set(prev_list))
                                    dictt2[ user["screen_name"] ] = queryy
                                except Exception:
                                    print 'yo3', " ", flag2
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
                                if( int(status["retweeted"])==1 ):
                                   retweet += 1
                                else:
                                   tweet += 1 

                            tweets_edit = 0 
                            for obj in mapp_username_list[ username ]:
                                for obj2 in mapp_username_list[ username ]:
                                    if( edit_distance(obj.gettextt(), obj2.gettextt()) >= 5 ):
                                        tweets_edit += 1

                            tweets_edit /= 2
                            fri = user["friends_count"]
                            foll = user["followers_count"] 
                            ratio =  "%.10f" %  ( float(foll) / (fri + foll) )
                            fri_comm = "%.10f" % ( float(len(inter)) / len(queryy) )
                            if( tweet>0 ):
                                tweet_retweet = "%.10f" % ( float(retweet) / tweet )
                            else:
                                tweet_retweet = 0 

                            #print 'reached here 3'
                            print str(user["friends_count"]) + "," + str(user["followers_count"]) + ",", 
                            #print 'reached here 4'
                            print str(ratio) + "," + str(user["favourites_count"]) + ",",
                            print str(user["statuses_count"]) + "," + str(user["verified"]), ",",
                            print str(noofurl) + "," + str(retweet), ",", str(fri_comm), ",", str(tweet_retweet), ",", str(tweets_edit)

                            outputt.write(str(user["friends_count"]) + "," + str(user["followers_count"]) + "," + str(ratio) + "," + str(user["favourites_count"]) + "," + str(user["statuses_count"]) + "," + str(user["verified"]) + "," + str(noofurl) + "," + str(retweet) + "," + str(fri_comm) + "," + str(tweet_retweet) + "," + str(tweets_edit) + "\n")
                except TwitterError as e:
                    stst = ''
                    flag3 = 0
                    for pp in e[0]:
                        if( pp=='{' or flag3 == 1 ):
                           stst += pp
                           flag3 = 1

                    stst = stst.split(':')
                    op =  stst[3][1] + stst[3][2]
                    print op
                    if( op == "17" ):
                        flag = 1
                        outputt.write("-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "," + "-1" + "\n")
                        continue
                    print 'yo', " ", flag
                    time.sleep(60)
    
    time.sleep(timeinterval)