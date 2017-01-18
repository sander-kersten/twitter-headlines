import tweepy, json
from tweepy import Stream
from tweepy.streaming import StreamListener
from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open('data.txt', 'a') as f:
                data=json.loads(data)
                user=data['user']
                user_id=user['id']
                data=api.user_timeline(user_id=user_id,count=200)
                for d in data:
                    f.write(d.text+'\n')
                    print(d.text+'\n')
                return True
        except BaseException as e:
            print("Error", str(e))
            return True

Items = ['nieuws', 'nos', 'nrc', 'krant', 'nieuws', 'anp', 'telegraaf', 'telegraaf', 'dagblad', 'courant', 'dagblad', 'journaal', 'journaal',
       'npo', 'actueel', 'vrt', 'stubru', 'canvas', 'radio', 'persbericht', 'reyerslaat', 'terzaketv', 'pauw', 'nieuwsuur', 'teletekst', 'rtl']
Items += [I.upper() for I in Items]
Items +=[I.capitalize() for I in Items]
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(languages=["nl"], track=Items)
