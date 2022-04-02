from pyrogram import Client
from pyrogram.types import Message

from client.api import ProdilAPI


class ProDil(Client, Message):
    admins = (635568322,)

    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            session_name=name,
            config_file=f"{name}.ini",
            workers=8,
            plugins=dict(root="probot/plugins"),
            workdir="probot",
        )

    async def start(self):
        await super().start()

    async def stop(self, *args):
        await super().stop()


api = ProdilAPI(config_file="prodil.ini")
