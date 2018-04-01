import tweepy
import json
import math
import glob
import csv
import zipfile
import zlib
from tweepy import TweepError
from time import sleep

with open('api_keys.json') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)

us_list = []
inputt = open('tweet_links.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

for user in us_list:
        username = user.strip() 
        username = username.strip('\n')
        username = username.split('/')
        username = username[3]
        user = username.lower()

        print user
        output_file = 'Dump/' + '{}.json'.format(user)
        output_file_short = 'Dump2/' + '{}_short.json'.format(user)

        with open('TweetCap/' + user + '.json') as f:
            ids = json.load(f)
         
        print ids
        print('total ids: {}'.format(len(ids)))

        all_data = []
        start = 0
        end = 100
        limit = len(ids)
        limit = float(limit)
        i = int(math.ceil(limit / 100))

        for go in range(i):
            print('currently getting {} - {}'.format(start, end))
            sleep(6)  # needed to prevent hitting API rate limit
            id_batch = ids[start:end]
            start += 100
            end += 100
            tweets = api.statuses_lookup(id_batch)
            for tweet in tweets:
                all_data.append(dict(tweet._json))

        print('metadata collection complete')
        print('creating master json file')
        with open(output_file, 'w') as outfile:
            json.dump(all_data, outfile)

        def is_retweet(entry):
            return 'retweeted_status' in entry.keys()

        def get_source(entry):
            if '<' in entry["source"]:
                return entry["source"].split('>')[1].split('<')[0]
            else:
                return entry["source"]

        results = []
        with open(output_file) as json_data:
            data = json.load(json_data)
            for entry in data:
                t = {
                    "created_at": entry["created_at"],
                    "text": entry["text"],
                    "in_reply_to_screen_name": entry["in_reply_to_screen_name"],
                    "retweet_count": entry["retweet_count"],
                    "favorite_count": entry["favorite_count"],
                    "source": get_source(entry),
                    "id_str": entry["id_str"],
                    "is_retweet": is_retweet(entry)
                }
                results.append(t)

        print('creating minimized json master file')
        with open(output_file_short, 'w') as outfile:
            json.dump(results, outfile)