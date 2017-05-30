import oauth2
import json
from pprint import pprint

def oauth_req(url, key, secret, http_method="GET", post_body='', http_headers=None):
    CONSUMER_KEY= '3iE2s0lUcpvxJ2Y8Pw5yTNCxy'
    CONSUMER_SECRET= 'KCDtlpUpuwBGLccZuWQjBqPClcHUtB02bXUSwkBVPOGQVeZ8Ib'
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json',
 '866749513096187904-J7oRHFNEbOlONVkVpEwVwfHhMPVtdgX', 'BAYSveXH9P8W7APdjtOrCcy89tMN2YwMHKeUkQYmKgwpw' )

print "hola bonito :3"

print home_timeline