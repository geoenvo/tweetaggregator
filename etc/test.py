#this script running TWEEPY and GOT cron job

def test():
    import django
    django.setup()
    from aggregator.cron import tweet_scheduled_job
    tweet_scheduled_job()
