import asyncio
import logging
import sqlite3
import hashlib
import feedparser

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, CHANNELS, RSS_FEEDS

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# ---------------- DATABASE ---------------- #

db = sqlite3.connect("sportsnews.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS posted(
id TEXT PRIMARY KEY
)
""")

db.commit()

# ---------------- HASHTAGS ---------------- #

def hashtags(title):

    t = title.lower()

    tags = []

    if "football" in t or "premier league" in t or "arsenal" in t or "chelsea" in t or "liverpool" in t or "manchester" in t:
        tags.append("#Football")

    if "nba" in t or "basketball" in t or "lakers" in t:
        tags.append("#NBA")

    if "tennis" in t or "wimbledon" in t:
        tags.append("#Tennis")

    if "f1" in t or "formula" in t:
        tags.append("#Formula1")

    if not tags:
        tags.append("#Sports")

    return " ".join(tags)

# ---------------- DUPLICATE CHECK ---------------- #

def already_posted(uid):

    cursor.execute("SELECT id FROM posted WHERE id=?", (uid,))

    return cursor.fetchone() is not None

def save(uid):

    cursor.execute("INSERT INTO posted VALUES(?)", (uid,))

    db.commit()

# ---------------- FORMAT ---------------- #

def build_message(item):

    title = item.title

    link = item.link

    tag = hashtags(title)

    text = f"""
🏆 <b>BREAKING SPORTS NEWS</b>

📰 <b>{title}</b>

👉 Read More:
{link}

{tag}
"""

    return text.strip()

# ---------------- RSS CHECK ---------------- #

async def check_news():

    while True:

        try:

            for feed in RSS_FEEDS:

                news = feedparser.parse(feed)

                for item in news.entries[:5]:

                    uid = hashlib.md5(item.link.encode()).hexdigest()

                    if already_posted(uid):
                        continue

                    msg = build_message(item)

                    for channel in CHANNELS:

                        try:

                            await bot.send_message(channel, msg)

                        except Exception as e:

                            print(e)

                    save(uid)

                    print("Posted:", item.title)

        except Exception as e:

            print(e)

        await asyncio.sleep(30)

# ---------------- START ---------------- #

async def main():

    asyncio.create_task(check_news())

    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
