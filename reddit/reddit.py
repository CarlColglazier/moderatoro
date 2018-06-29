import praw
import json
import base64
import zlib

class RedditSession:
    def __init__(self,
                 client_id, client_secret,
                 username, password, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            password=password,
            username=username,
            user_agent=user_agent
        )

    def get_usernotes(self, community):
        usernotes = json.loads(self.reddit.subreddit(community).wiki['usernotes'].content_md)
        usernotes = base64.b64decode(usernotes['blob'])
        usernotes = zlib.decompress(usernotes).decode()
        usernotes = json.loads(usernotes)
        return usernotes

    def stream(self, communities):
        return self.reddit.subreddit('+'.join(communities)).stream
