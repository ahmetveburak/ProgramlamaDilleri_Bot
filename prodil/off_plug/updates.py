from functools import partial
from pyrogram import filters, Client
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)

from prodil.BotConfig import ProDil

from prodil.models.model import session, Documents, Links, Books, Questions, Users
from prodil.utils.myfilters import (
    lngFilter,
    lvlFilter,
    lclFilter,
    resFilter,
    plang,
    common,
)
from prodil.utils.helpers import make_buttons
from prodil.utils.queries import History
from datetime import datetime


@ProDil.on_message(filters.media & filters.private)
async def check_doc(cl: Client, msg: Message):
    print(f"{msg.document.file_name}\n{msg.document.file_id}\n")

    doc = session.query(Documents).filter(Documents.path == msg.document.file_name).first()
    doc.file_id = msg.document.file_id
    session.add(doc)
    session.commit()
    # BQADBAADTAcAAmW0aFGQf8YzXodANRYE
    # BQACAgQAAxkBAAIEhWAmmhCzaGna0bVq0jzJiweOlcPfAAKOCgACI8U4UeomuYjaiH15HgQ
    # BQACAgQAAxkBAAIEhWAmmhCzaGna0bVq0jzJiweOlcPfAAKOCgACI8U4UeomuYjaiH15HgQ


@ProDil.on_message()
async def check_doc(cl: Client, msg: Message):
    print(msg.date)
    print(type(msg.date))