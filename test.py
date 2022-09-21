"""
adapted from: https://twarc-project.readthedocs.io/en/latest/api/library/
"""

# imports
import datetime
import os
import argparse

from typing import Tuple, Optional

from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened

from flask import Flask, request, render_template, jsonify
from get_followers import get_user_following_tweets

import re

import botometer

def parser():
    # argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument('-e', '--env', type=str,
        default='.env', help='environment configuration file that contains \
        user keys for twitter api v2')
    args = ap.parse_args()
    return args

# flask instance
app = Flask(__name__)

# twarc instance placeholder
t = None

pattern = re.compile('[\W_]+', re.UNICODE)

def run_results(search_results):
    res = ''
    for page in search_results:
        # Do something with the whole page of results:
        # print(page)
        # or alternatively, "flatten" results returning 1 tweet at a time, with expansions inline:
        for tweet in ensure_flattened(page):
            # print tweet text
            # res = res + '\n' + re.sub('[\W_]+', ' ', tweet['text']) + '\n'
            res = res + '\n' + tweet['text'] + '\n'
        # Stop iteration prematurely, to only get 1 page of results.
        break
    return res

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/form_post', methods=['POST', 'GET'])
def form_post():
    if (request.method == 'POST'):
        if (request.form['id'] == 'search-bar'):
            query = request.form['query']
            if (query):
                search_results = t.search_recent(query=query, start_time=None, 
                    end_time=None, max_results=10)
                res = run_results(search_results)
                return jsonify(result=res)
        if (request.form['id'] == 'user-search'):
            query = request.form['query']
            if (query):
                user_ids = get_user_following_tweets([query], t, 10, 5)
                return jsonify(result=str([key for key in user_ids[query]['following'].keys()]))


    if (request.method == 'GET'):
        print('get')

    return ("nothing")

if __name__ == "__main__":
    
    # get arguments
    args = parser()

    # parse configuration file
    f = open(args.env)
    toks = [line.split('=')[1].strip('\n') for line in f]

    # initialize twarc2 instance
    t = Twarc2(
        toks[1], # consumer token
        toks[2], # consumer secret
        toks[3], # access token
        toks[4], # access token secret
        toks[0]) # bearer token

    rapidapi_key = 'ef553c612emsh0aab3806e0dc54cp1fdb75jsn595045496df5'
    twitter_app_auth = {
        'consumer_key': 'rNYaIMBoelVLAJEJIh4DtZaQS',
        'consumer_secret': 'h4zsiN5O1XGzLWokMfphmN2yu3IjHK18LJ6dc7WVLbDnxa4xhY',
        'access_token': '1567967854271827970-i2mvPFTRg8UPqvHzVZYZKZwdBPTamz',
        'access_token_secret': 'NBCNSyXAmQfQWAMQe7qAwPWPdVuhh7HawMdX07tH6R4O1',
    }
    
    bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

    # Check a single account by screen name
    result = bom.check_account('@sophiagdelia')

    # start flask app
    app.run(port=8000)