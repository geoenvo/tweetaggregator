#!/usr/bin/env bash

source ~/.virtualenvs/tweetaggregator/bin/activate
cd $(dirname $0)/tweetaggregator
python manage.py runserver 0.0.0.0:8003
