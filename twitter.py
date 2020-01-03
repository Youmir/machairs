import os
import tweepy
import json
from tweepy import Stream
from tweepy.streaming import StreamListener
from textblob import TextBlob

consumer_key = "YQZrmBP4urKbsooOjlIj27xCw"
consumer_secret = "iE0dpl8H6NV5ynh0y6vF6sAKnzeMPKWZ1A9WQDi6puugvZyFwx"
access_token = "170886795-lRFn2z292CzQpY5RyWu1Y7EROqedUYzpSDxPJGMW"
access_token_secret = "Ee5rSPbVrKCTWd1JM5RO8CrK0p1X4zSqOKctT90OSvWQf"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class listener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        # Filter out non-English Tweets
        if data.get("lang") != "en": 
            return True
        try:
            timestamp = data['timestamp_ms']            
            # Get longer 280 char tweets if possible
            if data.get("extended_tweet"):
                tweet = data['extended_tweet']["full_text"]
            else:
                tweet = data["text"]
            url = "https://www.twitter.com/i/web/status/"+data["id_str"]
            user = data["user"]["screen_name"]
            verified = data["user"]["verified"]                  
            write_to_csv([timestamp, tweet, user, verified, url])
             
        except KeyError as e:
            print("Keyerror:", e)

        return True

    def on_error(self, status):
        print(status)

    def stream_and_write(table, track=None):
        try:
            twitterStream = Stream(auth, listener(),tweet_mode='extended')
            twitterStream.filter(track=["AAPL", "AMZN", "UBER"])
        except Exception as e:
            print("Error:", str(e))
            time.sleep(5)

ts = TextBlob(tweet).sentiment
print(ts.subjectivity, ts.polarity) # Subjectivity, Sentiment Scores
