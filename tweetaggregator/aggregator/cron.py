import sys
from datetime import datetime, timedelta

from django.conf import settings
from django.utils.encoding import smart_str

import tweepy
from tweepy import OAuthHandler

from .models import Source, Twitter
import got


def tweet_scheduled_job():
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    access_token = settings.ACCESS_TOKEN
    access_secret = settings.ACCESS_SECRET
    max_tweets = settings.MAX_TWEETS

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    sources = Source.objects.filter(status='ACTIVE', type='TWITTER')

    for active_source in sources:
        if active_source.method == "TWEEPY":
            keywords = active_source.keywords.all()
            for a_keyword in keywords:
                query = a_keyword.keyword
                searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
                for status in searched_tweets:
                    tweet_localcreatedtime = status.created_at + timedelta(hours=7)
                    diff = datetime.now() - tweet_localcreatedtime
                    diff_hours = diff.total_seconds() / 3600
                    if diff_hours <= 1:
                        tweet_text = status.text.translate(non_bmp_map)
                        tweet_text = "{}".format(smart_str(tweet_text))
                        tweet_id = status.id_str
                        tweet_created = status.created_at
                        user_id = status.user.id
                        user_name = status.user.name
                        user_screen_name = status.user.screen_name
                        user_utc_offset = status.user.utc_offset
                        user_coordinates = ''
                        ##if status.coordinates:
                        ##user_coordinates = user_coordinates
                        new_twitter = Twitter(
                            tweet_text=tweet_text,
                            keyword=a_keyword,
                            tweet_id=tweet_id,
                            tweet_created=tweet_created,
                            user_id=user_id,
                            user_name=user_name,
                            user_screen_name=user_screen_name,
                            user_utc_offset=user_utc_offset,
                            user_coordinate=user_coordinates
                        )
                        new_twitter.save()
        if active_source.method == "GOT":
            if (active_source.username == '' and active_source.since == None and active_source.until == None):
                keywords = active_source.keywords.all()
                for a_keyword in keywords:
                    query = a_keyword.keyword
                    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setMaxTweets(max_tweets)
                    searched_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                    for status in searched_tweets:
                        tweet_createdtime = status.date
                        diff = datetime.now() - tweet_createdtime
                        diff_hours = diff.total_seconds() / 3600
                        if diff_hours <= 1:
                            tweet_text = status.text
                            tweet_text = "{}".format(smart_str(tweet_text))
                            tweet_id = status.id
                            tweet_created = status.date
                            #user_id = status.user.id
                            user_name = ''
                            user_screen_name = status.username
                            #user_utc_offset = ''
                            user_coordinates = ''
                            new_twitter = Twitter(
                                tweet_text=tweet_text,
                                keyword=a_keyword,
                                tweet_id=tweet_id,
                                tweet_created=tweet_created,
                                #user_id=user_id,
                                user_name=user_name,
                                user_screen_name=user_screen_name,
                                #user_utc_offset=user_utc_offset,
                                user_coordinate=user_coordinates
                            )
                            new_twitter.save()

            if (active_source.username != '' and active_source.since == None and active_source.until == None):
                username = active_source.username
                keywords = active_source.keywords.all()
                for a_keyword in keywords:
                    query = a_keyword.keyword
                    tweetCriteria = got.manager.TweetCriteria().setUsername(username).setQuerySearch(query).setMaxTweets(max_tweets)
                    searched_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                    for status in searched_tweets:
                        tweet_text = status.text
                        tweet_text = "{}".format(smart_str(tweet_text))
                        tweet_id = status.id
                        tweet_created = status.date
                        #user_id = status.user.id
                        user_name = ''
                        user_screen_name = status.username
                        #user_utc_offset = ''
                        user_coordinates = ''
                        new_twitter = Twitter(
                            tweet_text=tweet_text,
                            keyword=a_keyword,
                            tweet_id=tweet_id,
                            tweet_created=tweet_created,
                            #user_id=user_id,
                            user_name=user_name,
                            user_screen_name=user_screen_name,
                            #user_utc_offset=user_utc_offset,
                            user_coordinate=user_coordinates
                        )
                        new_twitter.save()
