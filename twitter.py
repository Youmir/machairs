import os
import tweepy
import json
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = "YQZrmBP4urKbsooOjlIj27xCw"
consumer_secret = "iE0dpl8H6NV5ynh0y6vF6sAKnzeMPKWZ1A9WQDi6puugvZyFwx"
access_token = "170886795-lRFn2z292CzQpY5RyWu1Y7EROqedUYzpSDxPJGMW"
access_token_secret = "Ee5rSPbVrKCTWd1JM5RO8CrK0p1X4zSqOKctT90OSvWQf"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


api.update_status("Tweepy tweets for test #py ")