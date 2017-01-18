import tweepy, json
from tweepy import Stream
from tweepy.streaming import StreamListener
from config import *
from string import printable

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
mentioned = []
Tweets=[]

with open('data.txt') as f:
    for l in f.readlines():
        words = l.split()
        tweet=''
        for x in l.strip():
            if x in printable:
                tweet+=x
        if tweet and not tweet.startswith('RT '):
            Tweets.append(tweet)
        for word in words:
            if word.startswith('@'):
                mentioned.append(word)

mentioned = set(mentioned)

with open('data.txt', 'w') as f:
    f.write('\n'.join(Tweets))
    i=0
    for user in mentioned:
        screen_name = user[1:-1]
        i+=1
        try:
            data=api.user_timeline(screen_name=screen_name, count=200, include_rts=True)
            for Tweet in data:
                tweet=''
                for x in Tweet.text:
                    if x in printable:
                        tweet+=x
                f.write(tweet+'\n')
        except tweepy.error.TweepError:
            print("Fetched ", str(i), "of", str(len(mentioned)), "timelines")
