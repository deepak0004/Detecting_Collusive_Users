import pickle
import time
from twitter import *

#-----------------------------------------------------------------------
# twitter-retweets
#  - print who has retweeted tweets from a given user's timeline
#-----------------------------------------------------------------------

config = {}
execfile("config.py", config)
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

us_list = []

inputt = open('users.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

for username in us_list: 
        username = username.strip('\n')
        #outputt.write(username + ",")
        flag = 0
        while( flag == 0 ):
            try:
            	results = twitter.statuses.user_timeline(screen_name = username)
				
				#-----------------------------------------------------------------------
				# loop through each of my statuses, and print its content
				#-----------------------------------------------------------------------
				for status in results:
					print "@%s %s" % (user, status["text"])

					#-----------------------------------------------------------------------
					# do a new query: who has RT'd this tweet?
					#-----------------------------------------------------------------------
					flag2 = 0
                    while( flag2 == 0 ):
                        try:
							retweets = twitter.statuses.retweets._id(_id = status["id"])
                            flag2 = 1
                        except Exception:
                            time.sleep(60) 
					for retweet in retweets:
     			        print " - retweeted by %s" % (retweet["user"]["screen_name"])	
			except Exception:
                time.sleep(60)	