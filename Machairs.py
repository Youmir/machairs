from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import twitter_credentials
from tweepy import API
from tweepy import Cursor
import numpy as np 
import pandas as pd 


### Class Twitter Client
class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth = TwitterAuth().auth_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self,num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    def get_friend_list(self,num_friend):
        friend_list= []
        for friend in Cursor(self.twitter_client.friends,id=self.twitter_user).items(num_friend):
            friend_list.append(friend)
            return friend_list
    
    def get_home_timeline(self,num_tweets):
        timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(num_tweets):
            timeline_tweets.append(tweet)
        return timeline_tweets

    def get_twitter_client_api(self):
        return self.twitter_client

### Class Twitter authentification
class TwitterAuth():

    def auth_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY_TWITTER,twitter_credentials.CONSUMER_SECRET_TWITTER)
        auth.set_access_token(twitter_credentials.ACCESS_KEY_TWITTER,twitter_credentials.ACCESS_SECRET_TWITTER)
        return auth

### Class Twitter 
class TwitterListener(StreamListener):
    """
    Class for streaming and processing live tweets
    """
    def __init__(self,fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename


    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True
    
    def on_error(self,status):
        if status == 420:
            #return False in case rate limit occurs
            return False
        print(status)
    

### Class Twitter Streamer
class TwitterStreamer():
    """
    Class to print tweet
    """
    def __init__(self):
        self.twitter_auth = TwitterAuth()

    def stream_tweets(self,fetched_tweets_filename, hashtag_list):
        #this handles twitter auth and connection to twitter streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_auth.auth_twitter_app()

        stream = Stream(auth,listener)
        stream.filter(track=hashtag_list)
    

class TweetAnalyzer:
    """
    Functions for analyzing the tweets.
    """
    def tweets_to_data_frame(self,tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['Tweets'])

        df['id']=np.array([tweet.id for tweet in tweets])

        return df

if __name__ == "__main__":
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="realDonaldTrump", count=20)
    
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    print(df.head(10))
    #print(tweets[0].retweet_count)
    #print(dir(tweets[0])


