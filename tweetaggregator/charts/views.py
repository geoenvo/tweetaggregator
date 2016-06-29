from django.shortcuts import render_to_response
from aggregator.models import *
import calendar

def index(request, user):
    #S = Source.objects.all()
    T = Twitter.objects.all()
    #K = Keyword.objects.all()

    date = []
    for item in T:
        if item.user_screen_name == user:
            date.append(item.tweet_created.month)
            pass

    first_crwl = min(date)
    last_crwl = max(date)
    month_no = range(first_crwl, last_crwl + 1)

    extra_serie = {}
    xdata = []
    ydata = []
    for item in month_no:
        xdata.append(calendar.month_name[item])
        ydata.append(date.count(item))

    color_list = ['#5d8aa8', '#e32636', '#efdecd', '#ffbf00', '#ff033e', '#a4c639',
                  '#b2beb5', '#8db600', '#7fffd4', '#ff007f', '#ff55a3', '#5f9ea0']
    extra_serie2 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "color_list": color_list
    }
    xdata2 = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries",
             "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata2 = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]

    extra_serie3 = {}
    xdata3 = [1,2,3,4]
    ydata3 = [4,7,5,5]

    chartdata = {'x': xdata, 'name': 'tweets', 'y': ydata, 'extra': extra_serie}
    chartdata2 = {'x': xdata2, 'y1': ydata2, 'extra1': extra_serie2}
    chartdata3 = {'x': xdata3, 'name': 'tweets', 'y': ydata3, 'extra': extra_serie3}
    charttype = "multiBarChart"
    charttype2 = "pieChart"
    charttype3 = "lineChart"
    chartcontainer = 'multibarchart_container'
    chartcontainer2 = 'piechart_container'
    chartcontainer3 = 'linechart_container'
    data = {
        'charttype': charttype,
        'charttype2': charttype2,
        'charttype3': charttype3,
        'chartdata': chartdata,
        'chartdata2': chartdata2,
        'chartdata3': chartdata3,
        'chartcontainer': chartcontainer,
        'chartcontainer2': chartcontainer2,
        'chartcontainer3': chartcontainer3,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
        'extra2': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
        'extra3': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
                'jquery_on_ready': False,
        }
    }
    return render_to_response('charts/index.html', data)