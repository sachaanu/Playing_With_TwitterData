import oauth2 as oauth
import urllib.request as urllib
import csv
from csv import writer
import json
import time

api_key = "YaqIAhet1pXbPh7LxS6lRUKRg"
api_secret = "3BcAGwpUwv7TteNzOnhYeSIKlvjl2GDlMwqITQzUHvU4sVxRNy"
access_token_key = "364708179-ZVzGv2EgqZQoUkra4vigFaT457RvUKBEMeXUCQtK"
access_token_secret = "8cgL8qN31VbcSz5UUk4r0pKSnpHo5UHW3Bgd4C39BBwg5"

_debug=0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

#####get big ben clock tweets id
def fetch_bigben():
  url = "https://api.twitter.com/1.1/search/tweets.json?q=big_ben_clock&count=100&result_type=recent"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  return response

id_list=[]
re=fetch_bigben()
re_j=json.load(re)
re_j=re_j['statuses']
for a in re_j:
  id_list.append(a["id"])
#####end of big ben

#####get tweets about Super Bowl
tweets_num=500 # number of tweets we want
parameters = []
js=[]
for i in range(tweets_num/100):
  url = "https://api.twitter.com/1.1/search/tweets.json?q='Trump'&lang=en&count=100&result_type=recent&max_id="+str(id_list[2*i])
  response = twitterreq(url, "GET", parameters)
  re_j=json.load(response)
  re_j=re_j['statuses']
  js.append(re_j)
  time.sleep(1)

ids=[]
screen_name=[]
followers=[]
listed=[]
retweet=[]
inreplyto=[]
favorite=[]
friends=[]
text=[]

for tweets in js:
  for tweet in tweets:
    if tweet.get('user'):
        ids.append(tweet['user']['id']) 
        retweet.append(tweet['retweet_count'])
        favorite.append(tweet['favorite_count'])
        inreplyto.append(tweet['in_reply_to_screen_name'])
        friends.append(tweet['user']['friends_count'])
        screen_name.append(tweet['user']['screen_name'])
        followers.append(tweet['user']['followers_count'])
        listed.append(tweet['user']['listed_count'])
        text.append(tweet['text'])
####################################################

#######output tweets file
out = open('tweets.csv','wb')
print >> out, 'ids, screen_name, followers, retweet, inreplyto, favorite, friends, listed, text'

rows = zip(ids, screen_name, followers, retweet, inreplyto, favorite, friends, listed, text)

csv = writer(out)

for row in rows:
    values = [(value.encode('utf8') if hasattr(value, 'encode') else value) for value in row]
    csv.writerow(values)

out.close()
