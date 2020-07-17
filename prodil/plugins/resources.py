from functools import partial
from pyrogram import Filters, Message, Client, CallbackQuery
from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup

from prodil.models.model import Documents, Links, Books, Questions
from prodil.BotConfig import ProDil

command = partial(Filters.command, prefixes="/")


@ProDil.on_message(Filters.media)
async def book_update(client: Client, message: Message):
    if message.from_user.id == ProDil.OWNER_ID:
        book = Documents.objects(path=message.document.file_name).first()

        if book:
            book.update(file_id=message.document.file_id)
            book.save()

            await client.send_message(
                chat_id=message.chat.id,
                text=f"Dosya Adı: {book.name}\nfile_id başarıyla güncellendi.\n",
            )
        else:
            await client.send_message(
                chat_id=message.chat.id,
                text="Yeni kaynak eklemek istiyorsun fakat bu fonksiyon henüz mevcut değil.",
            )
    else:
        await client.send_message(
            chat_id=message.chat.id, text="Henüz kaynak eklemek için yetkin yok."
        )


# TODO
query: list = []


@ProDil.on_message(command("yeniekle"))
async def new_resource(client: Client, message: Message):
    if message.from_user.id == ProDil.OWNER_ID:
        book = Documents.objects(path=message.document.file_name).first()

        if book:
            book.update(file_id=message.document.file_id)
            book.save()

            await client.send_message(
                chat_id=message.chat.id,
                text=f"Dosya Adı: {book.name}\nfile_id başarıyla güncellendi.\n",
            )
        else:
            await client.send_message(
                chat_id=message.chat.id,
                text="Yeni kaynak eklemek istiyorsun fakat bu fonksiyon henüz mevcut değil.",
            )
    else:
        await client.send_message(
            chat_id=message.chat.id, text="Henüz kaynak eklemek için yetkin yok."
        )
