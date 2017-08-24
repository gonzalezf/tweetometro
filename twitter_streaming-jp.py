#  -*- coding: utf-8 -*-

# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

def datos_tweet(tweet):
    try:
        if 'text' in tweet.keys(): # only messages contains 'text' field is a tweet
            id_tw = str(tweet['id']) # This is the tweet's id
            fecha_tw = tweet['created_at'].encode('utf-8') # when the tweet posted
            if 'extended_tweet' in tweet.keys():
                texto_tw = tweet['extended_tweet']['full_text'].encode('utf-8') # content of the tweet
            else:
                texto_tw = tweet['text'].encode('utf-8')
            menciones = []
            for mencion in tweet['entities']['user_mentions']:
                if 'screen_name' in mencion.keys():
            	       menciones.append(mencion['screen_name'].encode('utf-8'))
            hashtags = []
            for hashtag in tweet['entities']['hashtags']:
                if 'text' in hashtag.keys():
            	       hashtags.append(hashtag['text'].encode('utf-8'))
    except Exception as e:
        print(e)
        return False
    return id_tw,fecha_tw,texto_tw,menciones,hashtags

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '1624072998-Gw8q7UMnczGRUDlhqzgUv24OzdYMGXgOiBP4fPA'
ACCESS_SECRET = 'JVOKlqH54WRjRr6fuLxPGRd8Fp6ZQFVJzmW6NUOrgu75d'
CONSUMER_KEY = 'aga3WCVl43kZitf8TfoS9ICZe'
CONSUMER_SECRET = 'Xa1VL2Vs8mxptElVWlQHzB3BZhVJ6j3Srab9P3a9yncig56JIR'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
#iterator = twitter_stream.statuses.filter(locations="-76.113,-55.379,-70.214,-18.428") # rectangulo de coordenadas que 'encierran' a Chile Continental
#iterator = twitter_stream.statuses.filter(locations="-70.928,-33.769,-70.433,-33.172") # el área de Santiago y alrededores
#iterator = twitter_stream.statuses.filter(track='transporte publico santiago,transporte público santiago,transportes santiago,metrosantiago,metro santiago,transantiago')
iterator = twitter_stream.statuses.filter(track='nyctsubway,nyc train subway, nyc subway, new york subway')

# Print each tweet in the stream to the screen
# Here we set it to stop after getting 1000 tweets.
# You don't have to set it to stop, but can continue running
# the Twitter API to collect data for days or even longer.
global_count = 0
while True:
    print('\n\n\n----------------- Tweets acumulados: '+str(global_count)+' -----------------\n\n\n')
    tweet_count = 100
    for tweet in iterator:
        # Twitter Python Tool wraps the data returned by Twitter
        # as a TwitterDictResponse object.
        # We convert it back to the JSON format to print/score
        # print (json.dumps(tweet))
        if 'place' in tweet.keys() or True:
            if True: # si el tweet es de la zona de Chile (sin este filtro, aparecen algunos tweets de Brasil):
                try:
                    tweet_id,tweet_fecha,tweet_texto,tweet_menciones,tweet_hashtags = datos_tweet(tweet)
                except:
                    print('*Error cargando info desde tweet.*')
                    continue
                tweet_count -= 1
                #txt = open('tweets_chile_jp/'+tweet_id+'.txt', 'wb') # para tweets sin filtro
                #txt = open('tweets_transportes/'+tweet_id+'.txt', 'wb') # para tweets que mencionen al metro de santiago
                txt = open('tweets_nyctsubway/bruto/'+tweet_id+'.txt', 'wb')
                txt.write(repr(tweet).encode('utf-8'))
                txt.close()
                txt = open('tweets_nyctsubway/filtrado/'+tweet_id+'.txt', 'wb')
                txt.write(tweet_fecha)
                txt.write('\r\n'.encode('utf-8'))
                txt.write(tweet_texto)
                txt.write('\r\n'.encode('utf-8'))
                for mention in tweet_menciones: # mention es @usuario
                    txt.write(mention)
                    txt.write('\r\n'.encode('utf-8'))
                txt.write('\r\n'.encode('utf-8'))
                for hashtag in tweet_hashtags: # hashtag es #algo
                    txt.write(hashtag)
                    txt.write('\r\n'.encode('utf-8'))
                txt.close()
                print(str(tweet_id)+': "'+str(tweet_texto.decode('utf-8'))+'"')
        # The command below will do pretty printing for JSON data, try it out
        # print json.dumps(tweet, indent=4)

        if tweet_count <= 0:
            global_count += 100
            break
