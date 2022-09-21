# imports
import datetime
import json
import os
import argparse

from typing import Tuple, Optional, Iterable

from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened, flatten

def get_user_following_tweets(
    users: Iterable[str],
    _twarc: Twarc2,
    num_following: int=10,
    num_tweets: int=10,
    verbose: bool=False
    ) -> dict:

    # get requested user bios
    user_bio = _twarc.user_lookup(users,
        usernames=True)
    
    # id list
    ids = []

    # get user ids from bios
    for bio in user_bio:
        ids.append(bio['data'][0]['id'])

    # empty dict
    user_ids = {}

    # for each requested user fetch 'num_following' users for
    # each of those requested users
    for id, user in zip(ids, users):
        followed = _twarc.following(id, max_results=num_following)

        for page in followed:
            # initialize dict for current user
            user_ids[user] = {'id': id, 'following': {}}
            
            for follower in flatten(page):
                # add to nested dictionary of user following
                user_ids[user]['following'][
                    follower['username']] = {'id': follower['id'],
                    'tweets': []}

            # Stop iteration prematurely, to only get 1 page of results.
            break

    # for each requested user fetch following users' tweets in the
    # previously defined dictionary, 'user_ids'
    for user, info in user_ids.items():
        # print(info['following'])
        for following_user, following_info in info['following'].items():
            following_id = following_info['id']
            # get timeline for current following of the given user
            timeline = _twarc.timeline(following_id, max_results=num_tweets)

            for page in timeline:
                for tweet in flatten(page):
                    # append to tweet for given user for given following
                    user_ids[user]['following'][
                        following_user]['tweets'].append(tweet['text'])
                break

    return user_ids

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

    ret = get_user_following_tweets([args.user], t, args.num_users, args.num_tweets)

    f = open('out.txt', 'w')
    f.write(json.dumps(ret))
    f.close()

    # print(ret)

    # user_bio = t.user_lookup([args.user],
    #     usernames=True)
    
    # ids = []

    # for bio in user_bio:
    #     ids.append(bio['data'][0]['id'])

    # user_ids = {}
    
    # for id in ids:
    #     followed = t.following(id, max_results=args.num_users)

    #     for page in followed:
    #         # Do something with the whole page of results:
    #         # print(page)
    #         for follower in flatten(page):
    #             # print tweet text
    #             # print(follower['username'], ": ", 
    #             #     follower['id'])
    #             user_ids[follower[
    #                 'username']] = follower['id']
    #         # Stop iteration prematurely, to only get 1 page of results.
    #         break
        
    # for username, id in user_ids.items():
    #     timeline = t.timeline(id, max_results=args.num_tweets)

    #     # print username
    #     print("{}: ".format(username))

    #     for page in timeline:
    #         # Do something with the whole page of results:
    #         # print(page)
    #         for tweet in flatten(page):
    #             print(tweet['text'])

    #     # Stop iteration prematurely, to only get 1 page of results.
    #     break
