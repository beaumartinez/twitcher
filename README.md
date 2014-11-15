# Twitcher

Post a screenshot of your Twitch stream to Twitter.

## Prerequisites

1. [Create a Twitter app](https://dev.twitter.com/apps).
2. Enable write acccess.
3. Request your access token and secret.

## Usage

    ./twitcher.py <twitch_username> <twitter_consumer_key> <twitter_consumer_secret> <twitter_access_token> <twitter_access_secret>

If the stream is live, it'll post a screenshot.

For full usage you can run—

	./twitcher.py --help
