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

# Google NLP example
from naturalLanguageTest import sample_analyze_sentiment

# Google NLP API
from google.auth import load_credentials_from_file
from google.cloud import language_v1

ap = argparse.ArgumentParser()
ap.add_argument('-p', '--port', type=int,
    default=5000, help='web server port\
    number')
ap.add_argument('-i', '--ip', type=str,
    default='localhost', help='web server ip')
ap.add_argument('-fb', '--firebase_credentials', type=str,
    default='software-mini-project-a9313-firebase-adminsdk-48pev-1e2967e8a1.json',
    help='path to firebase credentials')
ap.add_argument('-tw', '--twitter_credentials', type=str,
    default='.env', help='path to file with twitter api v2 credentials')
ap.add_argument('-rk', '--rapidapi_key', type=str,
    default='.key', help='path to file with rapidapi key for botometer')
ap.add_argument('-go', '--google_credentials', type=str,
    default='software-mini-project-a9313-921cf5b1ff7d.json',
    help='path to google nlp api credentials')
args = ap.parse_args()

# set google credentials from provided file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(
    args.google_credentials)

# open user provided twitter credentials
f = open(args.twitter_credentials)

# get each credential
toks = [line.split('=')[1].strip('\n') for line in f]

BEARER_TOKEN=toks[0]
CONSUMER_KEY=toks[1] # API Key
CONSUMER_SECRET=toks[2] # API Secret
ACCESS_TOKEN=toks[3]
ACCESS_TOKEN_SECRET=toks[4]

f.close()

# open user provided rapid api credentials
f = open(args.rapidapi_key)

rapidapi_key = [line.split('=')[1].strip('\n') for line in f][0]

f.close()

twitter_app_auth = {
    'consumer_key': CONSUMER_KEY,
    'consumer_secret': CONSUMER_SECRET,
    'access_token': ACCESS_TOKEN,
    'access_token_secret': ACCESS_TOKEN_SECRET,
}

# intialize flask application
app = Flask(__name__)

# Fetch the service account key JSON file contents. Credential path will change depending on user. I need a .env file...
cred = credentials.Certificate(args.firebase_credentials)

def fetch_and_store_user_tweets(
    user_investigated: List[str],
    max_following: int=10,
    num_tweets: int=10
    ) -> None:

    # load google nlp client
    nlp_client = language_v1.LanguageServiceClient()

    # initialize Botomer
    analysis = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://software-mini-project-a9313-default-rtdb.firebaseio.com/'
    })

    # Twarc init, get list of IDs of accounts specified
    client = Twarc2(consumer_key = CONSUMER_KEY, 
        consumer_secret = CONSUMER_SECRET, 
        access_token=ACCESS_TOKEN, 
        access_token_secret=ACCESS_TOKEN_SECRET)

    lookup = client.user_lookup(user_investigated, usernames=True, expansions=None, tweet_fields=None, user_fields=None)
    ids = []
    for gen_object in lookup: # generator object
        for users in gen_object['data']: # each user searched, don't need the twarc data
            ids.append(users['id'])  # collect user IDs to see who everyone follows

    # free memory
    del lookup

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

    # free memory
    del accounts, ids, data_array, clean_data

    # output array for following user data
    outputs = []
    for i in range(min(max_following, len(following_usernames))):
        # run bot analysis on account
        scores = analysis.check_account('@' + following_usernames[i])

        # get user tweets
        timeline = client.timeline(following_ids[i], max_results=num_tweets)

        # initialize dictionary to store into all outputs
        tweets = {'sentiments': {}, 'botometer': scores}
        for gen_object in timeline: # generator object
            for tweet in gen_object['data']:
                tweets['sentiments'][tweet['id']] = {'text': tweet['text']}
            break

        outputs.append(tweets)

    # free ids
    del following_ids, analysis, client

    for (i, output) in enumerate(outputs):
        # go through each sentiment analysis field
        for id in output['sentiments'].keys():
            # perform sentiment analysis and store result into output dict
            #output['sentiments'][id]['analysis'] = len(tweet['text'])
            output['sentiments'][id]['analysis'] = sample_analyze_sentiment(nlp_client, tweet['text'])

        # create json object
        json_object = json.dumps(output, indent=4)

        # store scores in firebase
        ref = db.reference(user_investigated[0]) # only ever investigate one user
        users_ref = ref.child(following_usernames[i] + '-scores')
        users_ref.set(json.loads(json_object))

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
    # start flask application
    app.run(port=args.port, host=args.ip, debug=True)

if __name__ == "__main__":
    main()