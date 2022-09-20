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

# Pull in data from Firebase- List of accounts followed

# Run Botometer on followed accounts, store scores in Firebase (only averages?)

# Read in each tweet from a single account, run Natural Language API, store scores in Firebase (only averages?)

