import os
from dotenv import load_dotenv

load_dotenv()

# ===========================
# BOT SETTINGS
# ===========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ===========================
# CHANNELS
# ===========================

BREAKING_CHANNEL = "@breakingsportsnews"

FOOTBALL_CHANNEL = "@footballdnews"

WORLD_CHANNEL = "@sportworldupdate"

# ===========================
# RSS FEEDS
# ===========================

# General Sports
BREAKING_FEEDS = [

    "https://feeds.bbci.co.uk/sport/rss.xml",

    "https://www.reutersagency.com/feed/?best-topics=sports",

]

# Football Only
FOOTBALL_FEEDS = [

    "https://feeds.bbci.co.uk/sport/football/rss.xml",

]

# NBA / Tennis / Formula 1 / Others
WORLD_FEEDS = [

    "https://www.nba.com/rss/nba_rss.xml",

    "https://www.atptour.com/en/media/rss-feed/xml",

]

# ===========================
# POST DESTINATIONS
# ===========================

CHANNEL_FEEDS = {

    BREAKING_CHANNEL: BREAKING_FEEDS,

    FOOTBALL_CHANNEL: FOOTBALL_FEEDS,

    WORLD_CHANNEL: WORLD_FEEDS,

}

# ===========================
# BOT SETTINGS
# ===========================

CHECK_INTERVAL = 30

POST_PREVIEW = True
