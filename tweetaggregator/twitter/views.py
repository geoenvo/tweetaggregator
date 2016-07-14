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
    order = request.GET.get('order')
    sort = request.GET.get('sort')
    records = Twitter.objects.filter(user_screen_name=user)
    if order is None:
        order = "dsc"
        sort = 'tweet_created'
    if sort is not None:
        paging_order = order
        paging_sort = sort
        records = records.order_by(sort)
        if order == "dsc":
            records = records.reverse()
            order = "asc"
        else:
            order = "dsc"
    else :
        paging_order = order
        paging_sort = sort
    if Source.objects.filter(username=user).exists():
        user_tweets = zip(range(len(records) + 1)[1:], records)
        all_user_tweets = paginator_page(request, user_tweets)
        context = {
            'all_user_tweets': all_user_tweets,
            'username': user,
            'order': order,
            'sort': sort,
            'paging_order': paging_order,
            'paging_sort': paging_sort,
        }
    else :
        context = {}
    return render_to_response('twitter/user_crawled.html', context)

def all_users_retweets(request, tweet):
    # Get all retweet's users
    order = request.GET.get('order')
    sort = request.GET.get('sort')
    tweet_origin = Twitter.objects.filter(tweet_id=tweet)[0]
    records = Retweet.objects.filter(tweet_id=tweet_origin)
    if order is None:
        order = "dsc"
        sort = 'retweet_created'
    if sort is not None:
        paging_order = order
        paging_sort = sort
        records = records.order_by(sort)
        if order == "dsc":
            records = records.reverse()
            order = "asc"
        else:
            order = "dsc"
    else:
        paging_order = order
        paging_sort = sort
    retweet_user = zip(range(len(records) + 1)[1:], records)
    all_retweet_user = paginator_page(request, retweet_user)
    context = {
        'tweet_origin':tweet_origin,
        'all_retweet_user':all_retweet_user,
        'order': order,
        'sort': sort,
        'paging_order': paging_order,
        'paging_sort': paging_sort,
        }
    return render_to_response('twitter/user_retweets.html', context)

def all_crawled_tweets(request):
    # Get all crawled tweets
    order = request.GET.get('order')
    sort = request.GET.get('sort')
    records = Twitter.objects.all()
    if order is None:
        order = "dsc"
        sort = 'tweet_created'
    if sort is not None:
        paging_order = order
        paging_sort = sort
        records = records.order_by(sort)
        if order == "dsc":
            records = records.reverse()
            order = "asc"
        else:
            order = "dsc"
    else:
        paging_order = order
        paging_sort = sort
    Tweets = zip(range(len(records) + 1)[1:], records)
    all_tweets = paginator_page(request, Tweets)
    context = {
            'all_tweets': all_tweets,
            'order': order,
            'sort': sort,
            'paging_order': paging_order,
            'paging_sort': paging_sort,
        }
    return render_to_response('twitter/tweets_crawled.html', context)
















