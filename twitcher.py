#! /usr/bin/env python

from sys import argv
from cStringIO import StringIO

import requests
import tweepy


user = argv[1]
consumer_key = argv[2]
consumer_secret = argv[3]
access_token = argv[4]
access_secret = argv[5]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

twitter = tweepy.API(auth)

stream_data = requests.get('https://api.twitch.tv/kraken/streams/{}'.format(user))
stream = stream_data.json()
stream = stream['stream']

if stream:
    image_url = stream['preview']['large']
    image_url = image_url.replace('640x360', '1280x720')
    image_file = requests.get(image_url)
    image_file = StringIO(image_file.content)

    name = stream['channel']['status']
    name = name.strip()
    name = name.encode('utf-8')

    game = stream['game']
    game = game.encode('utf-8')

    url = stream['channel']['url']
    created_at = stream['created_at']

    tweet_content = '{} on Twitch (streaming {}) {}'.format(name, game, url)

    print tweet_content, image_url

    tweet_response = twitter.update_with_media('{}.jpg'.format(user), tweet_content, file=image_file)
else:
    print 'Offline'
