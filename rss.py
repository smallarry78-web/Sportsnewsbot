import hashlib
import feedparser
from database import db
from config import CHANNEL_FEEDS


class RSSFetcher:

    @staticmethod
    def get_hashtags(title):

        title = title.lower()

        tags = []

        football = [
            "football",
            "premier league",
            "champions league",
            "arsenal",
            "chelsea",
            "liverpool",
            "manchester",
            "real madrid",
            "barcelona",
            "goal",
            "fifa",
            "uefa"
        ]

        nba = [
            "nba",
            "basketball",
            "lakers",
            "warriors",
            "celtics",
            "bucks"
        ]

        tennis = [
            "tennis",
            "wimbledon",
            "atp",
            "wta",
            "us open",
            "roland garros"
        ]

        formula = [
            "formula",
            "f1",
            "grand prix",
            "verstappen",
            "hamilton"
        ]

        if any(word in title for word in football):
            tags.append("#Football")

        if any(word in title for word in nba):
            tags.append("#NBA")

        if any(word in title for word in tennis):
            tags.append("#Tennis")

        if any(word in title for word in formula):
            tags.append("#Formula1")

        if not tags:
            tags.append("#Sports")

        return " ".join(tags)

    @staticmethod
    def format_post(entry):

        title = entry.title.strip()

        link = entry.link

        tags = RSSFetcher.get_hashtags(title)

        return f"""🏆 <b>BREAKING SPORTS NEWS</b>

📰 <b>{title}</b>

👉 <a href="{link}">Read Full Story</a>

{tags}
"""

    @staticmethod
    def fetch():

        posts = []

        for channel, feeds in CHANNEL_FEEDS.items():

            for feed in feeds:

                try:

                    rss = feedparser.parse(feed)

                    if not rss.entries:
                        continue

                    for article in rss.entries[:10]:

                        uid = hashlib.md5(
                            article.link.encode()
                        ).hexdigest()

                        if db.is_posted(uid, channel):
                            continue

                        posts.append({
                            "channel": channel,
                            "id": uid,
                            "text": RSSFetcher.format_post(article)
                        })

                except Exception as e:

                    print(e)

        return posts
