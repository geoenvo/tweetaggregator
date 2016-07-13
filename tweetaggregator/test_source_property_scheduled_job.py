#this script running TWEEPY and GOT cron job

def test():
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tweetaggregator.settings')
    django.setup()
    from aggregator.cron import source_property_scheduled_job
    source_property_scheduled_job()

if __name__ == '__main__':
    test()
