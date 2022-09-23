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

from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened

from flask import Flask, request, render_template, jsonify

# Twitter API
import requests
import os
import json

from naturalLanguageTest import sample_analyze_sentiment

# make bearer token an environmental variable later
BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAPJ5gwEAAAAASl5uDiBWeiW5F6C1QDLisPvO0nY%3DtEKTLYqOILQVpFNn7zA6cpfG6q1rqoJixOoKgGelkoKzxtKcID"
CONSUMER_KEY="rNYaIMBoelVLAJEJIh4DtZaQS" # API Key
CONSUMER_SECRET="h4zsiN5O1XGzLWokMfphmN2yu3IjHK18LJ6dc7WVLbDnxa4xhY" # API Secret
ACCESS_TOKEN="1567967854271827970-qDLS7TZDu5EhWpIMPOz0hZfqiRhDV1"
ACCESS_TOKEN_SECRET="fGuOMB9lOVybCtyxuMAGZ1eo86nt7hLFsvBj597O2jtKE"
credential_path = "C:/Users/sophi/Documents/Senior Design/service-account-file.json"

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

# Fetch the service account key JSON file contents. Credential path will change depending on user. I need a .env file...
cred = credentials.Certificate(credential_path)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://software-mini-project-a9313-default-rtdb.firebaseio.com/'
})

# Twarc init, get list of IDs of accounts specified
client = Twarc2(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

def fetch_and_store_user_tweets(
    user_investigated: List[str],
    max_following: int=10,
    num_tweets: int=10
    ) -> None:

    lookup = client.user_lookup(user_investigated, usernames=True, expansions=None, tweet_fields=None, user_fields=None)
    ids = []
    for gen_object in lookup: # generator object
        for users in gen_object['data']: # each user searched, don't need the twarc data
            ids.append(users['id'])  # collect user IDs to see who everyone follows

    # Get list of accounts specified user follows. Clean data.
    accounts = []
    data_array = []

    # fetch ids
    for id in ids:
        data = client.following(id)
        data_array.append(data)
        accounts.append(id)
    
    # fetch user data
    clean_data = []
    for gen_object in data_array:
        for user in gen_object:
            clean_data.append(user['data'])

    following_usernames = []
    following_ids = []
    for accounts in clean_data:
        for num_of_accounts in range(0,len(accounts)):
            following_usernames.append(accounts[num_of_accounts]['username']) # can also grab ID, grabbing username for simplicity
            following_ids.append(accounts[num_of_accounts]['id'])

    # output array for following user data
    outputs = []
    for i in range(min(max_following, len(following_usernames))):
        # run bot analysis on account
        scores = analysis.check_account('@' + following_usernames[i])

        # get user tweets
        timeline = client.timeline(following_ids[i], max_results=num_tweets)

        # initialize dictionary to store into all outputs
        tweets = {'username': following_usernames[i], 'sentiments': {}, 'botometer': scores}
        for gen_object in timeline: # generator object
            for tweet in gen_object['data']:
                tweets['sentiments'][tweet['id']] = {'text': tweet['text']}
            break

        outputs.append(tweets)

    for output in outputs:
        # go through each sentiment analysis field
        for id in output['sentiments'].keys():
            # perform sentiment analysis and store result into output dict
            output['sentiments'][id]['analysis'] = len(tweet['text'])
            # output['sentiments'][id]['analysis'] = sample_analyze_sentiment(tweet['text'])

        # # create json object
        # json_object = json.dumps(output, indent = 4)

        # # store scores in firebase
        # ref = db.reference(user_investigated[0]) # only ever investigate one user
        # users_ref = ref.child(username + '-scores')
        # users_ref.set(json.loads(json_object))

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
        if (request.form['id'] == 'user-search'):
            query = request.form['query']
            if (query):
                fetch_and_store_user_tweets([query])
                return jsonify(result="done")

    if (request.method == 'GET'):
        print('get')

    return ("nothing")

# main application code
def main() -> None:
    # get command line arguments
    args = parser()

    # start flask application
    app.run(port=args.port, host=args.ip)

if __name__ == "__main__":
    main()