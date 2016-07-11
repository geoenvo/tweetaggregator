from django.shortcuts import render_to_response
from aggregator.models import *
from django.db.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginator_page(request, data):
    # Make pagination
    paginator = Paginator(data, 20)
    page = request.GET.get('page')
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    return data_list

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

    users_list = zip(usernames, Crawled_Twitter, Tweet_Created, Retweets, Favorites, Twitter_Profile)
    all_users = paginator_page(request, users_list)

    context = {'all_users': all_users}
    return render_to_response('twitter/all_user.html', context)

def all_crawled_user(request, user):
    # Check if username actually exists in Source
    if Source.objects.filter(username=user).exists():
        User_Tweets = zip(range(len(Twitter.objects.filter(user_screen_name=user)) + 1)[1:], Twitter.objects.filter(user_screen_name=user))
        all_user_tweets = paginator_page(request, User_Tweets)
        context = {
            'all_user_Tweets': all_user_tweets,
            'username': user,
        }
    else :
        context = {}
    return render_to_response('twitter/user_crawled.html', context)

def all_crawled_tweets(request):
    # Get all crawled tweets
    Tweets = zip(range(len(Twitter.objects.all()) + 1)[1:], Twitter.objects.all())
    all_tweets = paginator_page(request, Tweets)
    context = {'all_tweets': all_tweets}
    return render_to_response('twitter/tweets_crawled.html', context)
















