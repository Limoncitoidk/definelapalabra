import tweepy
from getdef import *
from dotenv import load_dotenv
import os

load_dotenv('config.env')

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')

access_token = os.getenv('ACCESS_TOKEN')
access_secret = os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

#===========================================================

def getPalabra(texto):
    palabras = texto.split()
    for index in range(len(palabras)):
        if palabras[index] == "@DefineLaPalabra" and len(palabras) != (index+1):
            return palabras[index+1]

def enviarTweet(texto, status_id):
    if len(texto) > 280:
        last_tweet_id = status_id
        for i in range(0, len(texto), 280):
            split_text = texto[i:i+280]
            tweet = api.update_status(split_text, in_reply_to_status_id=last_tweet_id, auto_populate_reply_metadata=True)
            last_tweet_id = tweet.id_str
    else:
        api.update_status(texto, in_reply_to_status_id=status_id, auto_populate_reply_metadata=True)

#===========================================================

class TweetListener(tweepy.StreamListener):

    def on_connect(self):
        print("Conectado")

    def on_status(self, status):
        palabra = getPalabra(status.text)
        definicion = getDef(palabra)
        enviarTweet(definicion, status.id)

    def on_error(self, status_code):
        print("Error", status_code)

stream = TweetListener()
streamingApi = tweepy.Stream(auth=api.auth, listener=stream)

streamingApi.filter(
    track=["@DefineLaPalabra"]
)

