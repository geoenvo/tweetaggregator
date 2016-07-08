import sys
from datetime import datetime, timedelta

from django.conf import settings
from django.utils.encoding import smart_str

import tweepy
from tweepy import OAuthHandler

import got
from .models import Source, Twitter, Retweet, Source_Property


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
#usingTWEEPY
        if active_source.method == "TWEEPY":
            keywords = active_source.keywords.all()
            for a_keyword in keywords:
                query = a_keyword.keyword
                searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
                for status in searched_tweets:
                    tweet_id = status.id_str
                    if Twitter.objects.filter(tweet_id=tweet_id):
                        break
                    tweet_localcreatedtime = status.created_at + timedelta(hours=7)
                    diff = datetime.now() - tweet_localcreatedtime
                    diff_hours = diff.total_seconds() / 3600
                    if diff_hours <= 1:
                        tweet_text = status.text.translate(non_bmp_map)
                        tweet_text = "{}".format(smart_str(tweet_text))
                        tweet_created = tweet_localcreatedtime
                        user_id = status.user.id
                        user_name = status.user.name
                        user_screen_name = status.user.screen_name
                        user_URL = status.user.url
                        favorites = status.favorite_count
                        if hasattr(status, 'retweeted_status'):
                            retweets = status.retweet_count
                        user_utc_offset = status.user.utc_offset
                        user_coordinates = ''
                        if status.coordinates:
                            user_coordinates = status.coordinates['coordinates']
                        new_twitter = Twitter(
                            tweet_text=tweet_text,
                            keyword=a_keyword,
                            tweet_id=tweet_id,
                            tweet_created=tweet_created,
                            user_id=user_id,
                            user_name=user_name,
                            user_screen_name=user_screen_name,
                            user_utc_offset=user_utc_offset,
                            user_coordinate=user_coordinates,
                            user_URL=user_URL,
                            retweets=retweets,
                            favorites=favorites
                        )
                        new_twitter.save()
#usingGOT(GetOldTweets)
        if active_source.method == "GOT":
#usingGOT-by keywords
            if (active_source.username == '' and active_source.since == None and active_source.until == None):
                keywords = active_source.keywords.all()
                for a_keyword in keywords:
                    query = a_keyword.keyword
                    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query)
                    searched_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                    for status in searched_tweets:
                        tweet_id = status.id
                        if Twitter.objects.filter(tweet_id=tweet_id):
                            break
                        tweet_createdtime = status.date
                        diff = datetime.now() - tweet_createdtime
                        diff_hours = diff.total_seconds() / 3600
                        if diff_hours <= 1:
                            tweet_text = status.text
                            tweet_text = "{}".format(smart_str(tweet_text))
                            tweet_created = status.date
                            user_screen_name = status.username
                            user_name = ''
                            user_location = status.geo
                            retweets = status.retweets
                            favorites = status.favorites
                            new_twitter = Twitter(
                                tweet_text=tweet_text,
                                keyword=a_keyword,
                                tweet_id=tweet_id,
                                tweet_created=tweet_created,
                                user_name=user_name,
                                user_screen_name=user_screen_name,
                                user_location=user_location,
                                retweets=retweets,
                                favorites=favorites
                            )
                            new_twitter.save()
#usingGOT-by username
            if (active_source.username != '' and active_source.since == None and active_source.until == None):
                keywords = active_source.keywords.all()
                if not keywords:
                    username = active_source.username
                    tweetCriteria = got.manager.TweetCriteria().setUsername(username)
                    searched_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                    for status in searched_tweets:
                        tweet_id = status.id
                        if Twitter.objects.filter(tweet_id=tweet_id):
                            break
                        tweet_text = status.text
                        tweet_text = "{}".format(smart_str(tweet_text))
                        tweet_id = status.id
                        tweet_created = status.date
                        user_screen_name = status.username
                        user_name = ''
                        user_location = status.geo
                        retweets = status.retweets
                        favorites = status.favorites
                        new_twitter = Twitter(
                            tweet_text=tweet_text,
                            tweet_id=tweet_id,
                            tweet_created=tweet_created,
                            user_name=user_name,
                            user_screen_name=user_screen_name,
                            user_location=user_location,
                            retweets=retweets,
                            favorites=favorites
                        )
                        new_twitter.save()
#usingGOT-by username&keyword
            if (active_source.username != '' and active_source.since == None and active_source.until == None):
                username = active_source.username
                keywords = active_source.keywords.all()
                for a_keyword in keywords:
                    query = a_keyword.keyword
                    tweetCriteria = got.manager.TweetCriteria().setUsername(username).setQuerySearch(query)
                    searched_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                    for status in searched_tweets:
                        tweet_id = status.id
                        if Twitter.objects.filter(tweet_id=tweet_id):
                            break
                        tweet_text = status.text
                        tweet_text = "{}".format(smart_str(tweet_text))
                        tweet_created = status.date
                        user_name = ''
                        user_screen_name = status.username
                        user_location = status.geo
                        retweets = status.retweets
                        favorites = status.favorites
                        new_twitter = Twitter(
                            tweet_text=tweet_text,
                            keyword=a_keyword,
                            tweet_id=tweet_id,
                            tweet_created=tweet_created,
                            user_name=user_name,
                            user_screen_name=user_screen_name,
                            user_location=user_location,
                            retweets=retweets,
                            favorites=favorites
                        )
                        new_twitter.save()
#usingGOT-by user&daterange
            if (active_source.username != '' and (active_source.since != None or active_source.until != None)):
                keywords = active_source.keywords.all()
                if not keywords:
                    username = active_source.username
                    if (active_source.since != None and active_source.until == None):
                        since = active_source.since.strftime('%Y-%m-%d')
                        tweetCriteria = got.manager.TweetCriteria().setUsername(username).setSince(since)
                    if (active_source.since == None and active_source.until != None):
                        until = active_source.until.strftime('%Y-%m-%d')
                        tweetCriteria = got.manager.TweetCriteria().setUsername(username).setUntil(until)
                    if (active_source.since != None and active_source.until != None):
                        since = active_source.since.strftime('%Y-%m-%d')
                        until = active_source.until.strftime('%Y-%m-%d')
                        tweetCriteria = got.manager.TweetCriteria().setUsername(username).setSince(since).setUntil(until)
                    searched_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                    for status in searched_tweets:
                        tweet_id = status.id
                        if Twitter.objects.filter(tweet_id=tweet_id):
                            break
                        tweet_text = status.text
                        tweet_text = "{}".format(smart_str(tweet_text))
                        tweet_created = status.date
                        user_screen_name = status.username
                        user_name = ''
                        user_location = status.geo
                        retweets = status.retweets
                        favorites = status.favorites
                        new_twitter = Twitter(
                            tweet_text=tweet_text,
                            tweet_id=tweet_id,
                            tweet_created=tweet_created,
                            user_name=user_name,
                            user_screen_name=user_screen_name,
                            user_location=user_location,
                            retweets=retweets,
                            favorites=favorites
                        )
                        new_twitter.save()
#usingGOT-by keyword&daterange
            if (active_source.username == '' and (active_source.since != None or active_source.until != None)):
                keywords = active_source.keywords.all()
                for a_keyword in keywords:
                    query = a_keyword.keyword
                    if (active_source.since != None and active_source.until == None):
                        since = active_source.since.strftime('%Y-%m-%d')
                        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(since)
                    if (active_source.since == None and active_source.until != None):
                        until = active_source.until.strftime('%Y-%m-%d')
                        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setUntil(until)
                    if (active_source.since != None and active_source.until != None):
                        since = active_source.since.strftime('%Y-%m-%d')
                        until = active_source.until.strftime('%Y-%m-%d')
                        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(since).setUntil(until)
                    searched_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                    for status in searched_tweets:
                        tweet_id = status.id
                        if Twitter.objects.filter(tweet_id=tweet_id):
                            break
                        tweet_text = status.text
                        tweet_text = "{}".format(smart_str(tweet_text))
                        tweet_created = status.date
                        user_name = ''
                        user_screen_name = status.username
                        user_location = status.geo
                        retweets = status.retweets
                        favorites = status.favorites
                        new_twitter = Twitter(
                            tweet_text=tweet_text,
                            keyword=a_keyword,
                            tweet_id=tweet_id,
                            tweet_created=tweet_created,
                            user_name=user_name,
                            user_screen_name=user_screen_name,
                            user_location=user_location,
                            retweets=retweets,
                            favorites=favorites
                        )
                        new_twitter.save()
#usingGOT-by daterange&keyword&username
            if (active_source.username != '' and (active_source.since != None or active_source.until != None)):
                username = active_source.username
                keywords = active_source.keywords.all()
                for a_keyword in keywords:
                    query = a_keyword.keyword
                    if (active_source.since != None and active_source.until == None):
                        since = active_source.since.strftime('%Y-%m-%d')
                        tweetCriteria = got.manager.TweetCriteria().setUsername(username).setQuerySearch(query).setSince(since)
                    if (active_source.since == None and active_source.until != None):
                        until = active_source.until.strftime('%Y-%m-%d')
                        tweetCriteria = got.manager.TweetCriteria().setUsername(username).setQuerySearch(query).setUntil(until)
                    if (active_source.since != None and active_source.until != None):
                        since = active_source.since.strftime('%Y-%m-%d')
                        until = active_source.until.strftime('%Y-%m-%d')
                        tweetCriteria = got.manager.TweetCriteria().setUsername(username).setQuerySearch(query).setSince(since).setUntil(until)
                    searched_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                    for status in searched_tweets:
                        tweet_id = status.id
                        if Twitter.objects.filter(tweet_id=tweet_id):
                            break
                        tweet_text = status.text
                        tweet_text = "{}".format(smart_str(tweet_text))
                        tweet_created = status.date
                        user_name = ''
                        user_screen_name = status.username
                        user_location = status.geo
                        retweets = status.retweets
                        favorites = status.favorites
                        new_twitter = Twitter(
                            tweet_text=tweet_text,
                            keyword=a_keyword,
                            tweet_id=tweet_id,
                            tweet_created=tweet_created,
                            user_name=user_name,
                            user_screen_name=user_screen_name,
                            user_location=user_location,
                            retweets=retweets,
                            favorites=favorites
                        )
                        new_twitter.save()


def check_retweet_scheduled_job():
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    access_token = settings.ACCESS_TOKEN
    access_secret = settings.ACCESS_SECRET

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    sources = Twitter.objects.all()
    for source in sources:
        if source.retweets > 0:
            tweet_id = source.tweet_id
            tweetid = Twitter.objects.get(tweet_id=tweet_id)
            retweets = api.retweets(str(tweet_id), count=100)
            for a_retweet in retweets:
                retweet_id = a_retweet.id_str
                if Retweet.objects.filter(retweet_id=retweet_id):
                    break
                a_retweet_localcreatedtime = a_retweet.created_at + timedelta(hours=7)
                retweet_created = a_retweet_localcreatedtime
                user_id = a_retweet.user.id
                user_name = a_retweet.user.name
                user_screen_name = a_retweet.user.screen_name
                user_URL = a_retweet.user.url
                favorites = a_retweet.favorite_count
                followers_count = a_retweet.user.followers_count
                following_count = a_retweet.user.friends_count
                user_utc_offset = a_retweet.user.utc_offset
                user_coordinates = ''
                if a_retweet.coordinates:
                    user_coordinates = a_retweet.coordinates['coordinates']
                new_retweet = Retweet(
                    tweet_id=tweetid,
                    retweet_id=retweet_id,
                    retweet_created=retweet_created,
                    user_id=user_id,
                    user_name=user_name,
                    user_URL=user_URL,
                    user_screen_name=user_screen_name,
                    user_utc_offset=user_utc_offset,
                    user_coordinate=user_coordinates,
                    favorites=favorites,
                    followers_count=followers_count,
                    following_count=following_count
                        )
                new_retweet.save()


def source_property_scheduled_job():
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    access_token = settings.ACCESS_TOKEN
    access_secret = settings.ACCESS_SECRET

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    sources = Source.objects.filter(status='ACTIVE', type='TWITTER')

    for active_source in sources:
        if active_source.username != '':
            source = active_source
            name = active_source.username
            user = api.get_user(name)
            followers_count = user.followers_count
            following_count = user.friends_count
            new_source_property = Source_Property(
                            source=source,
                            followers_count=followers_count,
                            following_count=following_count,
                        )
            new_source_property.save()
