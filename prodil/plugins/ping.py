import time
from functools import partial
from pyrogram import Filters, Message, Client
from prodil.BotConfig import ProDil

command = partial(Filters.command, prefixes="!")


@ProDil.on_message(command("ping"))
async def ping(client: Client, message: Message):
    start = time.time()
    reply = await message.reply_text("...")
    delta_ping = time.time() - start
    await reply.edit_text(f"**Pong!** `{delta_ping * 1000:.3f} ms`")


# Test for single file
# @ProDil.on_message(command("gonder"))
# async def send_test(client: Client, message: Message):
#     await client.send_cached_media(
#         chat_id=message.chat.id,
#         file_id="",
#     )
