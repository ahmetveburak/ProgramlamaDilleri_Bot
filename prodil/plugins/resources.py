from functools import partial
from pyrogram import filters, Client
from pyrogram.types import Message
from prodil.models.model import session, Document
from prodil.BotConfig import ProDil

command = partial(filters.command, prefixes="/")


@ProDil.on_message(filters.me & filters.media & filters.private)
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
