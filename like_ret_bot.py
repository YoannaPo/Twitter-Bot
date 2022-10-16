
import time
import tweepy
import configparser
#from time import sleep

# ConfigParser is used to grab the authentication credentials from a config
# file making it safer when sharing the code.
config = configparser.ConfigParser()
config.read('config.ini')

apiKey = config['like_ret_bot']['api_key']
apiKeySecret = config['like_ret_bot']['api_secret']

bearerToken = config['like_ret_bot']['bearer_token']
# print("BT: "+bearerToken)

accessToken = config['like_ret_bot']['access_token']
accessTokenSecret = config['like_ret_bot']['access_token_secret']

# Gaining access and connecting to Twitter API using Credentials
client = tweepy.Client(bearerToken, apiKey, apiKeySecret,
                       accessToken, accessTokenSecret)

auth = tweepy.OAuth1UserHandler(
    apiKey, apiKeySecret, accessToken, accessTokenSecret)
api = tweepy.API(auth)

# if you add ["firstWord", "secondWord"] bot will be looking for specysfic words in a post/user name bot not as #hastag
search_terms = ["#firstWord", "#secondWord"]

# rule = tweepy.StreamRule(
#     "(#firstWord" OR "#secondWord OR #beauty) (-is:retweet -is:reply)")


class Mystream(tweepy.StreamingClient):
    def on_connect(self):
        print("Connected")

# reference tweet stores info if the tweet is original or it's a reply
# if the reference is set to None, probably the tweet is original
    def on_tweet(self, tweet):
        if tweet.referenced_tweets == None:
            print(tweet.text)
# added
            try:
                client.like(tweet.id)
                time(470)  # added
                client.retweet(tweet.id)
                time(470)  # added

            except Exception as error:
                print(error)
# added above

            time(470)


stream = Mystream(bearerToken)
# filtering the tweets => to do that: looping through each term
# (variable search_terms), and inside the loop we add stream rule  and then we pause term in here
# whole chunk of code will go through each term we specified at variable and then
# add them as rules which basically means we'll be  searching for tweets that contain at
# least one of these words
for term in search_terms:
    stream.add_rules(tweepy.StreamRule(term))

# below we excluding tweets that are being reffered
# and that aslo will give the class to the referenced tweets property
stream.filter(tweet_fields=["referenced_tweets"])
