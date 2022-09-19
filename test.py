import datetime
import os
import argparse

from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened

f = open('.env')
toks = [line.split('=')[1].strip('\n') for line in f]

# Your bearer token here
t = Twarc2(
    toks[1], # consumer token
    toks[2], # consumer secret
    toks[3], # access token
    toks[4], # access token secret
    toks[0]) # bearer token

# Start and end times must be in UTC
# start_time = datetime.datetime(2021, 3, 21, 0, 0, 0, 0, datetime.timezone.utc)
# end_time = datetime.datetime(2021, 3, 22, 0, 0, 0, 0, datetime.timezone.utc)
start_time = None
end_time = None

# search_results is a generator, max_results is max tweets per page, 100 max for full archive search with all expansions.
search_results = t.search_recent(query="dogs", start_time=start_time, end_time=end_time, max_results=10)

# Get all results page by page:
for page in search_results:
    # Do something with the whole page of results:
    # print(page)
    # or alternatively, "flatten" results returning 1 tweet at a time, with expansions inline:
    for tweet in ensure_flattened(page):
        # Do something with the tweet
        print(tweet)

    # Stop iteration prematurely, to only get 1 page of results.
    break
