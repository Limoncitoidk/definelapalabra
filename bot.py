import tweepy
from getdef import *
import os
from datetime import datetime
import threading
from boto.s3.connection import S3Connection

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']

access_token = os.environ['ACCESS_TOKEN']
access_secret = os.environ['ACCESS_SECRET']

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

class EnviarTweet():

    def __init__(self, texto):
        self.texto = texto
        
    def reply(self, status_id):
        split_text = self.cortar()
        last_tweet_id = status_id
        for x in split_text:
            tweet = api.update_status(x, in_reply_to_status_id=last_tweet_id, auto_populate_reply_metadata=True)
            last_tweet_id = tweet.id_str

    def tweet(self):
        split_text = self.cortar()
        tweet = api.update_status(split_text[0])
        if len(split_text) > 1:
            for x in range(len(split_text) - 1):
                last_tweet_id = tweet.id_str
                tweet = api.update_status(split_text[x+1], in_reply_to_status_id=last_tweet_id, auto_populate_reply_metadata=True)
                
            
    def cortar(self):
        split_text = []
        for i in range(0, len(self.texto), 280):
            split_text.append(self.texto[i:i+280])
        return split_text   

#===========================================================

def reloj():
    
    minutes = datetime.now().minute

    if minutes == 1 or minutes == 31:
        definicion = GetDef()
        nuevoTweet = EnviarTweet(definicion.random())
        nuevoTweet.tweet()

    timer = threading.Timer(60, reloj)
    timer.start()

timer = threading.Timer(60, reloj)
timer.start() 

#===========================================================

class TweetListener(tweepy.StreamListener):

    def on_connect(self):
        print("Conectado")

    def on_status(self, status):
        palabra = getPalabra(status.text)
        definicion = GetDef()
        nuevoTweet = EnviarTweet(definicion.set(palabra))
        nuevoTweet.reply(status.id)

    def on_error(self, status_code):
        print("Error", status_code)

stream = TweetListener()
streamingApi = tweepy.Stream(auth=api.auth, listener=stream)

streamingApi.filter(
    track=["@DefineLaPalabra"]
)

