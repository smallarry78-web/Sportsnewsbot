import asyncio
import hashlib
import logging
import sqlite3
import feedparser

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import (
    BOT_TOKEN,
    CHANNELS,
    ADMIN_ID,
    RSS_FEEDS,
)

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

# ==========================
# DATABASE
# ==========================

db = sqlite3.connect("sportsnews.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS posted(
    id TEXT PRIMARY KEY
)
""")

db.commit()

# ==========================
# CHANNEL BUTTONS
# ==========================

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📢 Breaking Sports News",
                url="https://t.me/breakingsportsnews",
            )
        ],
        [
            InlineKeyboardButton(
                text="⚽ Football Daily News",
                url="https://t.me/footballdnews",
            )
        ],
        [
            InlineKeyboardButton(
                text="🏆 Sports World Update",
                url="https://t.me/sportworldupdate",
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ I've Joined",
                callback_data="joined",
            )
        ],
    ]
)

# ==========================
# DUPLICATE CHECK
# ==========================

def article_id(link):

    return hashlib.md5(link.encode()).hexdigest()


def exists(uid):

    cursor.execute(
        "SELECT id FROM posted WHERE id=?",
        (uid,),
    )

    return cursor.fetchone() is not None


def save(uid):

    cursor.execute(
        "INSERT INTO posted VALUES(?)",
        (uid,),
    )

    db.commit()

# ==========================
# HASHTAGS
# ==========================

def get_tags(title):

    title = title.lower()

    if "football" in title:
        return "#Football"

    if "premier league" in title:
        return "#Football"

    if "arsenal" in title:
        return "#Football"

    if "chelsea" in title:
        return "#Football"

    if "liverpool" in title:
        return "#Football"

    if "nba" in title:
        return "#NBA"

    if "basketball" in title:
        return "#NBA"

    if "tennis" in title:
        return "#Tennis"

    if "formula" in title:
        return "#Formula1"

    return "#Sports"

# ==========================
# CHECK USER MEMBERSHIP
# ==========================

async def joined_all(user_id):

    try:

        for channel in CHANNELS:

            member = await bot.get_chat_member(
                channel,
                user_id,
            )

            if member.status in [
                "left",
                "kicked",
            ]:

                return False

        return True

    except Exception as e:

        print(e)

        return False# ==========================
# /START
# ==========================

@dp.message(CommandStart())
async def start(message: Message):

    if not await joined_all(message.from_user.id):

        await message.answer(
            "🚫 You must join all 3 channels before using this bot.\n\n"
            "Join the channels below and press ✅ I've Joined.",
            reply_markup=keyboard,
        )
        return

    await message.answer(
        "✅ Welcome to Sports News Auto Bot!\n\n"
        "You'll receive the latest sports updates."
    )


# ==========================
# VERIFY BUTTON
# ==========================

@dp.callback_query(F.data == "joined")
async def verify(callback: CallbackQuery):

    if await joined_all(callback.from_user.id):

        await callback.message.edit_text(
            "✅ Verification Successful!\n\n"
            "You now have access to Sports News Auto Bot."
        )

    else:

        await callback.answer(
            "❌ You haven't joined all required channels.",
            show_alert=True,
        )


# ==========================
# BUILD POST
# ==========================

def build_post(item):

    title = item.title

    link = item.link

    tags = get_tags(title)

    return f"""
🏆 <b>BREAKING SPORTS NEWS</b>

📰 <b>{title}</b>

👉 <a href="{link}">Read Full Story</a>

{tags}
"""


# ==========================
# CHECK RSS
# ==========================

async def rss_checker():

    while True:

        try:

            for feed in RSS_FEEDS:

                rss = feedparser.parse(feed)

                if not rss.entries:
                    continue

                for item in rss.entries[:10]:

                    uid = article_id(item.link)

                    if exists(uid):
                        continue

                    post = build_post(item)

                    for channel in CHANNELS:

                        try:

                            await bot.send_message(
                                chat_id=channel,
                                text=post,
                                disable_web_page_preview=False,
                            )

                        except Exception as e:

                            logging.error(
                                f"{channel}: {e}"
                            )

                    save(uid)

                    logging.info(
                        f"Posted: {item.title}"
                    )

        except Exception as e:

            logging.error(e)

        await asyncio.sleep(30)


# ==========================
# MAIN
# ==========================

async def main():

    asyncio.create_task(
        rss_checker()
    )

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())
