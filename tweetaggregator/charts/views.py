from django.shortcuts import render_to_response
from aggregator.models import *
import calendar
import numpy as np

def index(request, user):
    T = Twitter.objects.all()
    user = user.split(',')
    user = filter(None, user)
    user_index = 0
    user_list = []
    for item in T:
        user_list.append(item.user_screen_name)
    for item in user:
        if item not in user_list:
            user.remove(item)
    xdata = np.empty([len(user), 3, 0], dtype='float64')
    xdata = xdata.tolist()
    ydata = np.empty([len(user), 3, 0], dtype='float64')
    ydata = ydata.tolist()
    extra_serie = {}
    chartdata_list = []
    chartcontainer_list = []
    charttype_list = []

    # Iterate Username
    for username in user:
        date = []
        tweet_keyword = []
        tags_keyword = []
        for item in T:
            if item.user_screen_name == username:
                date.append(item.tweet_created.month)
                tweet_keyword.append(item.keyword.keyword)
                tags_keyword.append(item.tags_tweet.all())
                pass

        first_crwl = min(date)
        last_crwl = max(date)
        month_no = range(first_crwl, last_crwl + 1)
        keyword_list = sorted(set(tweet_keyword))
        uniq_tags = [i for sublist in tags_keyword for i in sublist]
        tags_list = sorted(set(uniq_tags))
        # Chart Type 0
        for item in month_no:
            xdata[user_index][0].append(calendar.month_name[item])
            ydata[user_index][0].append(date.count(item))
        # Chart Type 1
        n = 0
        for i in tags_list:
            for j in tags_keyword:
                if i in j:
                    n += 1
            xdata[user_index][1].append(str(i))
            ydata[user_index][1].append(n)
            n = 0
        u = 0
        for i in tags_keyword:
            if not i:
                u += 1
        if u > 0:
            xdata[user_index][1].append("empty tag")
            ydata[user_index][1].append(u)
        # Chart Type 2
        for item in keyword_list:
            xdata[user_index][2].append(item)
            ydata[user_index][2].append(tweet_keyword.count(item))
        # Next Username
        user_index += 1

    # Embed to Data
    data = {
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': True,
        }
    }
    chartdata = np.empty([len(user) * 3, 3], dtype='S100')
    chartdata = chartdata.tolist()
    for i in range(len(user)):
        for j in range(3):
            chartdata[i][j] = {'x': xdata[i][j], 'name': 'tweets', 'y': ydata[i][j], 'extra': extra_serie}
            chartdata_list.append(chartdata[i][j])
            if j % 2 == 0:
                charttype_list.append("multiBarChart")
            else:
                charttype_list.append("pieChart")

    data.update({'chartdata': chartdata_list})

    chartcontainer = np.empty([len(user) * 3, 3], dtype='S100')
    chartcontainer = chartcontainer.tolist()
    for i in range(len(user)):
        for j in range(3):
            chartcontainer[i][j] = 'username'+str(i)+'_type'+str(j)
            chartcontainer_list.append(chartcontainer[i][j])
    data.update({'chartcontainer': chartcontainer_list})

    data.update({'zipped_data': zip(charttype_list, chartdata_list, chartcontainer_list)})
    return render_to_response('charts/index.html', data)