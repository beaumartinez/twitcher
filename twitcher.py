#! /usr/bin/env python

from argparse import ArgumentParser
from cStringIO import StringIO

import requests
import tweepy


# 140 chars - (1 space, 22 for the link, 1 space, 22 for the image) = 94 chars
TWEET_LIMIT = 94


def get_args():
    parser = ArgumentParser(description='Post a screenshot of your Twitch stream to Twitter.')
    parser.add_argument('user', help='Twitch username')
    parser.add_argument('consumer_key', help='Twitter API consumer key')
    parser.add_argument('consumer_secret', help='Twitter API consumer secret')
    parser.add_argument('access_token', help='Twitter API access token')
    parser.add_argument('access_secret', help='Twitter API consumer access secret')

    args = parser.parse_args()

    return args


def _twitter_api(args):
    auth = tweepy.OAuthHandler(args.consumer_key, args.consumer_secret)
    auth.set_access_token(args.access_token, args.access_secret)

    twitter = tweepy.API(auth)

    return twitter


def _get_stream(user):
    stream_data = requests.get('https://api.twitch.tv/kraken/streams/{}'.format(user))
    stream = stream_data.json()
    stream = stream['stream']

    return stream


def _parse_status(stream):
    status = stream['channel']['status']
    status = status.strip()
    status = status.encode('utf-8')

    return status


def _parse_game(stream):
    game = stream['game']
    game = game.strip()
    game = game.encode('utf-8')

    return game


def _get_image(stream):
    image_url = stream['preview']['large']
    image_url = image_url.replace('640x360', '1920x1080')
    image_file = requests.get(image_url)
    image_file = StringIO(image_file.content)

    return image_url, image_file


def _parse_url(stream):
    url = stream['channel']['url']

    return url


def post_tweet(args):
    stream = _get_stream(args.user)

    if stream:
        status = _parse_status(stream)
        game = _parse_game(stream)
        url = _parse_url(stream)

        tweet_content = '{} live on Twitch (streaming {}) {}'.format(status, game, url)

        if len(tweet_content) > TWEET_LIMIT:
            print 'Long tweet. Trimming'
            tweet_content = '{} streaming {} on Twitch {}'.format(status, game, url)

            if len(tweet_content) > TWEET_LIMIT:
                print 'Still a long tweet. Trimming'
                tweet_content = '{} on Twitch {}'.format(status, url)

        image_url, image_file = _get_image(stream)

        print tweet_content, image_url

        twitter = _twitter_api(args)
        twitter.update_with_media('{}.jpg'.format(args.user), tweet_content, file=image_file)
    else:
        print 'Offline'


if __name__ == '__main__':
    args = get_args()
    post_tweet(args)
