from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import CHANNELS

router = Router()


def join_keyboard():
    buttons = [
        [InlineKeyboardButton(text="📢 Breaking Sports News", url="https://t.me/breakingsportsnews")],
        [InlineKeyboardButton(text="⚽ Football News", url="https://t.me/footballdnews")],
        [InlineKeyboardButton(text="🏆 Sports World Update", url="https://t.me/sportworldupdate")],
        [InlineKeyboardButton(text="✅ I've Joined", callback_data="check_join")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def user_joined(bot, user_id):

    for channel in CHANNELS:

        member = await bot.get_chat_member(channel, user_id)

        if member.status in ["left", "kicked"]:
            return False

    return True


@router.message(CommandStart())
async def start(message: Message):

    if not await user_joined(message.bot, message.from_user.id):

        await message.answer(
            "🚫 You must join all 3 channels before using this bot.",
            reply_markup=join_keyboard(),
        )

        return

    await message.answer(
        "✅ Welcome!\n\nYou now have access to Sports News Auto Bot."
    )


@router.callback_query(lambda c: c.data == "check_join")
async def check(callback: CallbackQuery):

    if await user_joined(callback.bot, callback.from_user.id):

        await callback.message.edit_text(
            "✅ Verification successful!\n\nWelcome to Sports News Auto Bot."
        )

    else:

        await callback.answer(
            "You haven't joined all channels yet.",
            show_alert=True,
        )
