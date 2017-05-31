import oauth2
import json
from pprint import pprint
import time
#query
#places: https://api.twitter.com/1.1/geo/reverse_geocode.json?lat=-33.447487&long=-70.673676
#tweets by place: https://api.twitter.com/1.1/search/tweets.json?q=place%3A47a3cf27863714de&granularity=country&count=100
#places2: https://api.twitter.com/1.1/geo/search.json?query=Chile   47a3cf27863714de
#chile: 47a3cf27863714de

def oauth_req(url, key, secret, http_method="GET", post_body='', http_headers=None):
    CONSUMER_KEY= '3iE2s0lUcpvxJ2Y8Pw5yTNCxy'
    CONSUMER_SECRET= 'KCDtlpUpuwBGLccZuWQjBqPClcHUtB02bXUSwkBVPOGQVeZ8Ib'
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    return content


def tweets_chile():
    max_id_chile= open('max_id_chile.txt', 'rw')
    since_id= max_id_chile.readline()
    max_id_chile.close()

    if (since_id==''):
        url= 'https://api.twitter.com/1.1/search/tweets.json?q=place%3A47a3cf27863714de%2C%20%40metrodesantiago&granularity=country&count=100&result_type=recent&include_entities=false'
    else:
        url= 'https://api.twitter.com/1.1/search/tweets.json?q=place%3A47a3cf27863714de%2C%20%40metrodesantiago&granularity=country&count=100&result_type=recent&include_entities=false&since_id='+since_id
    
    print url

    home_timeline = oauth_req(
        url,
        '866749513096187904-pa1we5ZbIDrdgEd8mYo5eani8z6CKxn',
        '7RtPFFALsLnIdCDkJ3qg9vAHZ0rBnXvdmMiT1pK1HVTHS')

    try:
        status = json.loads(home_timeline)['statuses']

        print 'se extrajeron: ',len(status), 'tweets\n'

        i=0
        for tweet in status:
            tweet_id= tweet['id_str']
            txt = open('tweets_chile/'+tweet_id+'.txt', 'w')
            txt.write(tweet['text'].encode('utf-8'))
            txt.close()

        #guardar id de ultimo tweet
        max_id= str(json.loads(home_timeline)['search_metadata']['max_id'])
        max_id_chile= open('max_id_chile.txt', 'w')
        max_id_chile.write(max_id)
        max_id_chile.close()

    except KeyError:
        print json.loads(home_timeline)



while (1):
    tweets_chile()
    print 'Esperando 1 minuto para actualizar...\n\n'
    time.sleep(60)



#print len(json.loads(home_timeline)['statuses'])
#print json.loads(home_timeline)['statuses']

#-56.56,-109.50,-17.50,-109.48,-17.50,-66.15,-56.56,-66.15,-56.58,-109.48

#-109.48,-56.56,-109.5,-17.5,-66.15,-17.5,-66.15,-56.56,-109.48,-56.56
