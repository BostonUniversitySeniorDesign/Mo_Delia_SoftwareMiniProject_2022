"""
adapted from: https://twarc-project.readthedocs.io/en/latest/api/library/
"""

# # imports
# import datetime
# import os
# import argparse

# from twarc.client2 import Twarc2
# from twarc.expansions import ensure_flattened

# # argument parser
# ap = argparse.ArgumentParser()
# ap.add_argument('-q', '--query', type=str,
#     required=True, help='user query')
# ap.add_argument('-n', '--num', type=int,
#     default=10, help='number of tweets to fetch')
# ap.add_argument('-e', '--env', type=str,
#     default='.env', help='environment configuration file that contains \
#     user keys for twitter api v2')
# args = ap.parse_args()

# # parse configuration file
# f = open(args.env)
# toks = [line.split('=')[1].strip('\n') for line in f]

# # Your bearer token here
# t = Twarc2(
#     toks[1], # consumer token
#     toks[2], # consumer secret
#     toks[3], # access token
#     toks[4], # access token secret
#     toks[0]) # bearer token

# # Start and end times must be in UTC
# # start_time = datetime.datetime(2021, 3, 21, 0, 0, 0, 0, datetime.timezone.utc)
# # end_time = datetime.datetime(2021, 3, 22, 0, 0, 0, 0, datetime.timezone.utc)
# start_time = None
# end_time = None

# # search_results is a generator, max_results is max tweets per page, 100 max for full archive search with all expansions.
# search_results = t.search_recent(query=args.query, start_time=start_time, 
#     end_time=end_time, max_results=args.num)

# # Get all results page by page:
# for page in search_results:
#     # Do something with the whole page of results:
#     # print(page)
#     # or alternatively, "flatten" results returning 1 tweet at a time, with expansions inline:
#     for tweet in ensure_flattened(page):
#         # print tweet text
#         print(tweet['text'])

#     # Stop iteration prematurely, to only get 1 page of results.
#     break

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/form_post', methods=['POST', 'GET'])
def form_post():
    if (request.method == 'POST'):
        if (request.form['id'] == 'search-bar'):
            print(request.form['query'])
            
    if (request.method == 'GET'):
        print('get')

    return ("nothing")

app.run(port=8000)