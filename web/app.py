from flask import Flask
from secret import *

import discord
import praw

app = Flask(__name__)
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    password=REDDIT_PASSWORD,
    username=REDDIT_USERNAME,
    user_agent=REDDIT_USER_AGENT
)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/reddit")
def reddit_func():
    return str([x for x in reddit.subreddit('all').emoji])
