#this script running TWEEPY and GOT cron job

def test():
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tweetaggregator.settings')
    django.setup()
    from aggregator.cron import tweet_scheduled_job
    tweet_scheduled_job()

if __name__ == '__main__':
    test()
