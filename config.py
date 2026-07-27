import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

CHANNELS = [
    os.getenv("CHANNEL_1"),
    os.getenv("CHANNEL_2"),
    os.getenv("CHANNEL_3"),
]

RSS_FEEDS = [

    "https://feeds.bbci.co.uk/sport/rss.xml",

    "https://feeds.bbci.co.uk/sport/football/rss.xml",

    "https://www.espn.com/espn/rss/news",

    "https://www.nba.com/rss/nba_rss.xml",

]
