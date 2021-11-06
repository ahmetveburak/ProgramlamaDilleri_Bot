from pyrogram import Client
from pyrogram.types import Message

# TODO package and install from github
from prodil_client.prodil_client.client import ProdilAPI

api = ProdilAPI(
        api_url="http://127.0.0.1:8000/api",
        email="admin@admin.com",
        password="1",
    )


class ProDil(Client, Message):
    OWNER_ID: int = 635568322
    CHATS: list = []

    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            session_name=name,
            config_file=f"{name}/{name}.ini",
            workers=8,
            plugins=dict(root=f"{name}/plugins"),
            workdir=f"{name}",
        )

        self.admins = {chat: {ProDil.OWNER_ID} for chat in ProDil.CHATS}

    async def start(self):
        await super().start()

    async def stop(self, *args):
        await super().stop()
