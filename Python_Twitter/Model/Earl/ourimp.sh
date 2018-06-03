#!/bin/bash

while true; do
  python generation_of_m.py
  python retweet_tweet_topics_3.py 
  python paper_final.py
  sleep 60
done