# imports
import datetime
import os
import argparse

from typing import Tuple, Optional

from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened, flatten

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--user", type=str,
        required=True, help="username to query")
    ap.add_argument("-nu", "--num_users", type=int,
        default=10, help="number of followers to query")
    ap.add_argument("-nt", "--num_tweets", type=int,
        default=10, help="number of tweets from each user")
    ap.add_argument("-e", "--env", type=str,
        default=".env", help="configuration file")
    args = ap.parse_args()

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

    user_bio = t.user_lookup([args.user],
        usernames=True)
    
    ids = []

    for bio in user_bio:
        ids.append(bio['data'][0]['id'])

    user_ids = {}
    
    for id in ids:
        followed = t.following(id, max_results=args.num_users)


        for page in followed:
            # Do something with the whole page of results:
            # print(page)
            for follower in flatten(page):
                # print tweet text
                # print(follower['username'], ": ", 
                #     follower['id'])
                user_ids[follower[
                    'username']] = follower['id']
            # Stop iteration prematurely, to only get 1 page of results.
            break
        