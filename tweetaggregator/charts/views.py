from django.shortcuts import render_to_response
from aggregator.models import *
import datetime
import calendar


def tweet_charts(request, users):
    usernames = users.split(',')
    usernames = filter(None, usernames)
    
    # Check if username actually exists in Source
    valid_usernames = []
    for username in usernames:
        if Source.objects.filter(username=username).exists():
            valid_usernames.append(username)
    valid_usernames = set(valid_usernames)

    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    tags = Twitter.tags_tweet.values()
    user_tweets = {}
    user_keywords = {}
    user_tags = {}
    for valid_username in valid_usernames:
        user_tweets[valid_username] = []
        user_keywords[valid_username] = []
        user_tags[valid_username] = []
        keywords = Keyword.objects.filter(source=Source.objects.filter(username=valid_username))
        # Get username's tweet count per month so far this year
        for month in range(1, current_month + 1):
            tweet_month_count = Twitter.objects.filter(user_screen_name=valid_username, tweet_created__year=current_year, tweet_created__month=month).count()
            user_tweets[valid_username].append([calendar.month_name[month], tweet_month_count])
        # Get username's tweet count per username's registered keywords
        for keyword in keywords:
            keyword_count = Twitter.objects.filter(user_screen_name=valid_username, keyword=keyword.id).count()
            user_keywords[valid_username].append([keyword.keyword, keyword_count])
        # Get username's tweet tags count and username's empty tags count
        for tag in tags:
            tag_count = Twitter.objects.filter(user_screen_name=valid_username, tags_tweet=tag['id']).count()
            if tag_count != 0:
                user_tags[valid_username].append([tag['name'],tag_count])
        emptytag_count =  Twitter.objects.filter(user_screen_name=valid_username, tags_tweet=None).count()
        user_tags[valid_username].append(['empty_tag',emptytag_count])
        
    # Convert to charts data format ([Chart_Type][Valid_Username])
    data = {
        'valid_usernames': valid_usernames,
        'charttype_Bar': 'multiBarChart',
        'charttype_Pie': 'pieChart',
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        }
    }
    extra_serie = {}
    xdata = [[],[],[]]
    ydata = [[],[],[]]
    for valid_username in valid_usernames:
        x = [[],[],[]]
        y = [[],[],[]]
        for n in range(len(user_tweets[valid_username])):
            x[0].append(user_tweets[valid_username][n][0])
            y[0].append(user_tweets[valid_username][n][1])
        for n in range(len(user_keywords[valid_username])):
            x[1].append(user_keywords[valid_username][n][0])
            y[1].append(user_keywords[valid_username][n][1])
        for n in range(len(user_tags[valid_username])):
            x[2].append(user_tags[valid_username][n][0])
            y[2].append(user_tags[valid_username][n][1])
        xdata[0].append(x[0])
        ydata[0].append(y[0])
        xdata[1].append(x[1])
        ydata[1].append(y[1])
        xdata[2].append(x[2])
        ydata[2].append(y[2])
    chartdata_list = [[],[],[]]
    chartcontainer_list = [[],[],[]]
    user = []
    for n, valid_username in zip(range(len(valid_usernames)),valid_usernames):
        chartdata_0 = {'x': xdata[0][n], 'y': ydata[0][n], 'extra': extra_serie}
        chartdata_1 = {'x': xdata[1][n], 'y': ydata[1][n], 'extra': extra_serie}
        chartdata_2 = {'x': xdata[2][n], 'y': ydata[2][n], 'extra': extra_serie}
        chartcontainer_0 = 'username' + str(n) + '_type0'
        chartcontainer_1 = 'username' + str(n) + '_type1'
        chartcontainer_2 = 'username' + str(n) + '_type2'
        chartdata_list[0].append(chartdata_0)
        chartdata_list[1].append(chartdata_1)
        chartdata_list[2].append(chartdata_2)
        chartcontainer_list[0].append(chartcontainer_0)
        chartcontainer_list[1].append(chartcontainer_1)
        chartcontainer_list[2].append(chartcontainer_2)
        user.append(valid_username)
    data.update({'type0': zip(user, chartdata_list[0], chartcontainer_list[0])})
    data.update({'type1': zip(user, chartdata_list[1], chartcontainer_list[1])})
    data.update({'type2': zip(user, chartdata_list[2], chartcontainer_list[2])})
    return render_to_response('charts/index.html', data)






