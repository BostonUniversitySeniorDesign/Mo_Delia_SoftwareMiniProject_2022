# Imports

# Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Natural Language
from google.cloud import language_v1

# Botometer / Flask
import botometer
from flask import Flask

#Twarc
import datetime
import os
import argparse

from typing import Tuple, Optional

from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened

from flask import Flask, request, render_template, jsonify

# Twitter API
import requests
import os
import json

# make bearer token an environmental variable later
BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAPJ5gwEAAAAASl5uDiBWeiW5F6C1QDLisPvO0nY%3DtEKTLYqOILQVpFNn7zA6cpfG6q1rqoJixOoKgGelkoKzxtKcID"
CONSUMER_KEY="rNYaIMBoelVLAJEJIh4DtZaQS" # API Key
CONSUMER_SECRET="h4zsiN5O1XGzLWokMfphmN2yu3IjHK18LJ6dc7WVLbDnxa4xhY" # API Secret
ACCESS_TOKEN="1567967854271827970-qDLS7TZDu5EhWpIMPOz0hZfqiRhDV1"
ACCESS_TOKEN_SECRET="fGuOMB9lOVybCtyxuMAGZ1eo86nt7hLFsvBj597O2jtKE"

# Get ID of user
users = ['sophiagdelia'] # change to be variable input. can only see public accounts
# client = Twarc2(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, bearer_token=bearer_token, connection_errors=0, metadata=True) 
# parse configuration file


# Twarc init, get list of IDs of accounts specified
client = Twarc2(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

lookup = client.user_lookup(users, usernames=True, expansions=None, tweet_fields=None, user_fields=None)
ids = []
for gen_object in lookup: # generator object
    for users in gen_object['data']: # each user searched, don't need the twarc data
        ids.append(users['id'])  # collect user IDs to see who everyone follows

# Get list of accounts specified user follows. Print accounts just for gigs.
accounts = []
for id in ids:
    following_gen_dict = client.following(id)
    accounts.append(id)
#print(accounts)
data_array = []
following = []

for id in accounts:
    data = client.following(id)
    data_array.append(data)
    
# print(data_array)
clean_data = []
for gen_object in data_array:
    for user in gen_object:
        clean_data.append(user['data'])

following_usernames = []
for accounts in clean_data:
    for num_of_accounts in range(0,len(accounts)):
        following_usernames.append(accounts[num_of_accounts]['username'])

print(following_usernames)
    #following.append(data['username'])
#     # For each account specified
#     for gen_object in following_gen_dict: # for each object of single account
#         # print(gen_object)
#         # print("\n")
#         users_followed = []
#         for users in gen_object['data']: # for each user followed
#             users_followed.append(users['username'])
# print(users_followed)

# main()


# following(self, user, user_id=None, max_results=1000, expansions=None, tweet_fields=None, user_fields=None, pagination_token=None)

# Pull in data from Firebase- List of accounts followed

# Run Botometer on followed accounts, store scores in Firebase (only averages?)

# Read in each tweet from a single account, run Natural Language API, store scores in Firebase (only averages?)

