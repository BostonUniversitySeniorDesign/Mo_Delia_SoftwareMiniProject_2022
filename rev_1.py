# Imports

# Typing
from typing import Union, List, Optional

# Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

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
credential_path = "C:/Users/sophi/Documents/Senior Design/service-account-file.json"

# Get ID of user
user_investigated = None
# user_investigated = ['sophiagdelia'] # change to be variable input. can only see public accounts
# client = Twarc2(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, bearer_token=bearer_token, connection_errors=0, metadata=True) 
# parse configuration file

rapidapi_key = 'ef553c612emsh0aab3806e0dc54cp1fdb75jsn595045496df5'
twitter_app_auth = {
    'consumer_key': CONSUMER_KEY,
    'consumer_secret': CONSUMER_SECRET,
    'access_token': ACCESS_TOKEN,
    'access_token_secret': ACCESS_TOKEN_SECRET,
}

# initialize Botomer
analysis = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# intialize flask application
app = Flask(__name__)

# Twarc init, get list of IDs of accounts specified
client = Twarc2(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

def fetch_and_store_user_tweets(
    user_investigated: List[str],
    max_following: int=10
    ):

    lookup = client.user_lookup(user_investigated, usernames=True, expansions=None, tweet_fields=None, user_fields=None)
    ids = []
    for gen_object in lookup: # generator object
        for users in gen_object['data']: # each user searched, don't need the twarc data
            ids.append(users['id'])  # collect user IDs to see who everyone follows

    # Get list of accounts specified user follows. Clean data.

    accounts = []
    # for id in ids:
    #     following_gen_dict = client.following(id)
    #     accounts.append(id)

    data_array = []
    # for id in accounts:
    for id in ids:
        data = client.following(id)
        data_array.append(data)
        accounts.append(id)
        
    clean_data = []
    for gen_object in data_array:
        for user in gen_object:
            clean_data.append(user['data'])

    following_usernames = []
    for accounts in clean_data:
        for num_of_accounts in range(0,len(accounts)):
            following_usernames.append(accounts[num_of_accounts]['username']) # can also grab ID, grabbing username for simplicity

    # Run Botometer on followed accounts, store scores in Firebase (only averages?)

    # Fetch the service account key JSON file contents. Credential path will change depending on user. I need a .env file...
    # cred = credentials.Certificate(credential_path)

    # # Initialize the app with a service account, granting admin privileges
    # firebase_admin.initialize_app(cred, {
    #     'databaseURL': 'https://software-mini-project-a9313-default-rtdb.firebaseio.com/'
    # })

    # # Check account by screen name

    ret = []
    json_array = []
    # for username in following_usernames:
    for i in range(min(max_following, len(following_usernames))):
        scores = analysis.check_account('@' + following_usernames[i])
        # scores = analysis.check_account('@' + username)
        ret.append(scores)
        # json_object = json.dumps(scores, indent = 4)
        # # store scores in firebase
        # ref = db.reference(user_investigated[0]) # only ever investigate one user
        # users_ref = ref.child(username + '-scores')
        # users_ref.set(json.loads(json_object))

    return ret

    # Read in each tweet from a single account, run Natural Language API, store scores in Firebase (only averages?)

    # TODO add google nlp api to get sentiment for 
    # each tweet and store into firebase

# argument parser
def parser():
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--port', type=int,
        default=5000, help='web server port\
        number')
    ap.add_argument('-i', '--ip', type=str,
        default='localhost', help='web server ip')
    args = ap.parse_args()
    return args

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/form_post', methods=['POST', 'GET'])
def form_post():
    if (request.method == 'POST'):
        # if (request.form['id'] == 'search-bar'):
        #     query = request.form['query']
        #     if (query):
        #         search_results = client.search_recent(query=query, start_time=None, 
        #             end_time=None, max_results=10)
        #         res = run_results(search_results)
        #         return jsonify(result=res)
        if (request.form['id'] == 'user-search'):
            query = request.form['query']
            if (query):
                data = fetch_and_store_user_tweets([query])
                return jsonify(result=str(data))

    if (request.method == 'GET'):
        print('get')

    return ("nothing")

# main application code
def main():
    # get command line arguments
    args = parser()

    # start flask application
    app.run(port=args.port, host=args.ip)

if __name__ == "__main__":
    main()