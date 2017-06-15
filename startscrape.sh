#!/usr/bin/env bash

source ~/.virtualenvs/tweetaggregator/bin/activate
cd $(dirname $0)/tweetaggregator
python test_tweet_scheduled_job.py
