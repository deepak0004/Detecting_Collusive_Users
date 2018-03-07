#-----------------------------------------------------------------------
# twitter-friends
#  - lists all of a given user's friends (ie, followees (following) ), the ones user is following
#-----------------------------------------------------------------------
from twitter import *

config = {}
execfile("config.py", config)
#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
us_list = []
dictt = {}

inputt = open('users.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

#outputt = open('user_following.txt', 'w', 0)
for username in us_list: 
        username = username.strip('\n')
        #outputt.write(username + ",")
        query = twitter.friends.ids(screen_name = username)

		#-----------------------------------------------------------------------
		# tell the user how many friends we've found.
		# note that the twitter API will NOT immediately give us any more 
		# information about friends except their numeric IDs...
		#-----------------------------------------------------------------------
        #outputt.write( str(len(query["ids"])) ) 
        print username, " ", len(query["ids"]), " ", len(username)
        dictt[ username ] = []
        if( len(query["ids"]) ):
			#-----------------------------------------------------------------------
			# now we loop through them to pull out more info, in blocks of 100.
			#-----------------------------------------------------------------------
            for n in range(0, len(query["ids"]), 98):
            	ids = [-1]
                ids.extend( query["ids"][n:n+98] )
                ids.append(-1)
                #print len(ids)
                #print ids
                subquery = twitter.users.lookup(user_id = ids)
                print len(ids), " ", len(subquery)
                for user in subquery:
                    #print str(user["screen_name"]), 
					#outputt.write( "," + str(user["screen_name"]) )
                    dictt[ username ].append( str(user["screen_name"]) ) 
        #outputt.write("\n")
        print len(dictt[username])

with open("user_and_who_he_following.dump", "wb") as fp:   #Pickling
	pickle.dump(dictt, fp)