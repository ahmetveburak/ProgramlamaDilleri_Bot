from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from functools import partial
from prodil.BotConfig import ProDil
from prodil.models.model import session, Documents, Questions

command = partial(filters.command, prefixes=["!", "/", "."])


@ProDil.on_message(command("test"))
async def mytest(client: Client, message: Message) -> None:
    a = session.query(Questions).filter(Questions.id == 1).first()
    print(
        f"{a.p_lang}\n",
        f"{a.level}\n",
        f"{a.lang}\n",
        f"{a.resources}\n",
    )
