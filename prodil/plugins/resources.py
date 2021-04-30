from functools import partial
from pyrogram import filters, Client
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from prodil.models.model import session, Document, Link, Book, Question
from prodil.BotConfig import ProDil

command = partial(filters.command, prefixes="/")

atropos = filters.create(lambda _, __, msg: msg.from_user.id in [635568322])


@ProDil.on_message(atropos & filters.media & filters.private)
async def book_update(client: Client, message: Message):
    # TODO
    print(message)
    book = session.query(Document).filter(Document.path == message.document.file_name).first()

    if book:
        book.file_id = message.document.file_id
        book.enabled = True
        await message.reply_text(text="Kaynak güncellendir ve aktifleştirildi.")
        session.commit()

    else:
        await message.reply_text(text="Kaynak güncellenemedi. Veritabanında böyle bir dosya bulunamadı.")
