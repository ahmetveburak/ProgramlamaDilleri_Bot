import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from probot.BotConfig import ProDil, api
from probot.utils.helpers import command


@ProDil.on_message(command("hakkinda") & filters.private)
async def bot_about(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text=(
            "Bu bot kâr amacı güdülmeksizin, faydalı olabilecek kaynakların "
            "kolayca ulaşılabilir olması için geliştirilmiştir. "
            "Burada bulunmasının iyi olacağını düşündüğünüz "
            "kaynaklar var ise geliştiricilere iletebilirsiniz."
            "\n\n__Mühendis Köyü kanalımıza katılabilirsiniz.__"
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "@musaitbiyerde", url="https://t.me/musaitbiyerde"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Mühendis Köyü", url="https://t.me/muhendiskoyu"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Kaynak Kodlar",
                        url="https://github.com/ahmetveburak/ProgramlamaDilleri",
                    )
                ],
            ]
        ),
    )


@ProDil.on_message(filters.document & filters.private)
async def bot_file_update(_: Client, message: Message):
    caption = getattr(message, "caption")
    create = api.create_resource(
        name=message.caption if caption else message.document.file_name,
        file_name=message.document.file_name,
        file_size=message.document.file_size,
        file_id=message.document.file_id,
        file_unique_id=message.document.file_unique_id,
    )

    text = "Dosya oluşturulurken veya güncellenirken bir hata oluştu."
    if create.status_code == 201:
        text = "Dosya başarıyla oluşturuldu veya güncellendi."

    reply_message = await message.reply_text(text=f"`{text}`")
    await asyncio.sleep(3)
    await reply_message.delete()
