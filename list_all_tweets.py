import tweepy
import json
from tweepy import OAuthHandler

consumer_key = "YaqIAhet1pXbPh7LxS6lRUKRg"
consumer_secret = "secret-key"

access_token = "364708179-ZVzGv2EgqZQoUkra4vigFaT457RvUKBEMeXUCQtK"
access_token_secret = "secret-token"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def process_or_store(tweet):
    print(json.dumps(tweet))
for tweet in tweepy.Cursor(api.user_timeline).items(50):
    process_or_store(tweet._json)
