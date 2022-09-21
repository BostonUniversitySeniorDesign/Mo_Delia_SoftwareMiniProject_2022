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
users = ['sophiagdelia','supersoph_3'] # change to be variable input
# client = Twarc2(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, bearer_token=bearer_token, connection_errors=0, metadata=True) 
# parse configuration file

client = Twarc2(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

lookup = client.user_lookup(users, usernames=True, expansions=None, tweet_fields=None, user_fields=None)
for gen_object in lookup: # generator object
    for users in gen_object['data']: # each user searched, don't need the twarc data
        print(users['id'])
    


# # Twarc Init
# def get_user_id():
#     lookup = client.user_lookup(users, usernames=True, expansions=None, tweet_fields=None, user_fields=None)
#     return lookup

# # Get list of accounts specified user follows. Print accounts just for gigs.
# # Get username(s) you want to look into. For now, local, eventually firebase. Can do up to 100.
# def get_following(user_id):
#     following_list = client.following(user_id)
#     return following_list

# def main():
#     user_id_gen_obj = get_user_id()
#     for user_id in user_id_gen_obj:
#         print(*user_id) # unpack
#     following = get_following(user_id)
#     for user in following:
#         print(*user)

# main()


# following(self, user, user_id=None, max_results=1000, expansions=None, tweet_fields=None, user_fields=None, pagination_token=None)

# Pull in data from Firebase- List of accounts followed

# Run Botometer on followed accounts, store scores in Firebase (only averages?)

# Read in each tweet from a single account, run Natural Language API, store scores in Firebase (only averages?)

