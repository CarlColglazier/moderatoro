import praw
import json
import base64
import zlib
import feedparser
import datetime
from bs4 import BeautifulSoup 

REDDIT_RSS = 'https://www.reddit.com/r/{}/new/.rss?sort=new&limit={}'
FEED_LIMIT = 5
PERIOD = 60

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

class Submission:
    """
    def __init__(self, title, subreddit, url, link, author):
        self.title = title
        self.subreddit = subreddit
        self.url = url
        self.link = link
        self.author = author
    """

    def __init__(self, dictionary):
        soup = BeautifulSoup(dictionary['description'], 'html.parser')
        mdclass = soup.find('div',class_='md')
        if mdclass is not None:
            mdclass.decompose()
        links = soup.find_all('a')
        if links[0].find('img'):
            # This could possibly be used to get the thumbnail.
            del links[0]
        self.title = dictionary['title']
        self.subreddit = links[1].get_text().strip()
        self.url = links[3]['href']
        self.link = links[2]['href']
        self.author = links[0].get_text().strip()
    
class SubmissionFeed:
    def __init__(self, communities, interval):
        self.communities = communities
        self.interal = interval
        self.last = (
            datetime.datetime.utcnow() - datetime.timedelta(minutes=PERIOD)
        ).timetuple()
        self.submissions = []

    def atom_feed(self):
        subs_list = '+'.join(self.communities)
        feed = feedparser.parse(
            REDDIT_RSS.format(subs_list, FEED_LIMIT)
        )
        return feed

    def new_submissions(self):
        feed = self.atom_feed()
        new = [Submission(x) for x in feed['entries'] if x['updated_parsed'] > self.last]
        self.last = datetime.datetime.utcnow().timetuple()
        return new

    def submission(self):
        if len(self.submissions) == 0:
            self.submissions = self.new_submissions()
        while len(self.submissions):
            yield self.submissions.pop(0)
