from django.shortcuts import render_to_response
from aggregator.models import *
from django.db.models import *
import datetime
import calendar

def all_user(request):
    # Get all username
    all_user = Source.objects.all()
    usernames = []
    Crawled_Twitter = []
    Tweet_Created = []
    Retweets = []
    Favorites = []
    Twitter_Profile = []
    # Calculate all attributes for each username
    for user in all_user :
        usernames.append(user.username)
        Crawled_Twitter.append(Twitter.objects.filter(user_screen_name=user.username).count())
        Tweet_Created.append(Twitter.objects.filter(user_screen_name=user.username).aggregate(Max('tweet_created')).get('tweet_created__max'))
        Retweets.append(Twitter.objects.filter(user_screen_name=user.username).aggregate(Sum('retweets')).get('retweets__sum'))
        Favorites.append(Twitter.objects.filter(user_screen_name=user.username).aggregate(Sum('favorites')).get('favorites__sum'))
        Twitter_Profile.append('https://twitter.com/' + user.username)
    context = {'all_data': zip(usernames, Crawled_Twitter, Tweet_Created, Retweets, Favorites, Twitter_Profile)}
    return render_to_response('twitter/all_user.html', context)

def all_crawled_user(request, user):
    # Check if username actually exists in Source
    if Source.objects.filter(username=user).exists():
        User_Tweets = Twitter.objects.filter(user_screen_name=user)
        context = {
            'User_Tweets': zip(range(len(User_Tweets) + 1)[1:], User_Tweets),
            'username': user,
        }
    else :
        context = {}
    return render_to_response('twitter/user_crawled.html', context)














