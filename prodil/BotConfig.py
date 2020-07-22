from pyrogram import Client, Message
from pyrogram import __version__
import configparser
from sshtunnel import SSHTunnelForwarder
import mongoengine

# Only for local development
# vps = configparser.ConfigParser()
# vps.read("prodil/vpsconfig.ini")
# print(vps.sections())
# server = SSHTunnelForwarder(
#     vps["MongoVPS"]["MONGO_HOST"],
#     ssh_username=vps["MongoVPS"]["MONGO_USER"],
#     ssh_password=vps["MongoVPS"]["MONGO_PASS"],
#     remote_bind_address=("127.0.0.1", 27017),
# )


class ProDil(Client, Message):
    OWNER_ID: int = 635568322
    CHATS: list = []

    def __init__(self):
        name = self.__class__.__name__.lower()
        print(f"NAME: {name}")
        super().__init__(
            session_name=name,
            config_file=f"{name}/{name}.ini",
            workers=8,
            plugins=dict(root=f"{name}/plugins"),
            workdir=f"{name}/sessions",
        )

        self.admins = {chat: {ProDil.OWNER_ID} for chat in ProDil.CHATS}

    async def start(self):
        mongoengine.register_connection(alias="core", name="prodil_test")

        # Only for local development
        # server.start()
        # mongoengine.register_connection(
        #     alias="core", name="prodil_test", port=server.local_bind_port
        # )
        await super().start()

        # me = await self.get_me()
        # for chat, admins in self.admins.items():
        #     async for admin in self.iter_chat_members(chat, filter="administrators"):
        #         admins.add(admin.user.id)

    async def stop(self, *args):
        mongoengine.disconnect(alias="core")
        # server.stop()
        await super().stop()

    # def is_admin(self, message: Message) -> bool:
    #     user_id = message.from_user.id
    #     chat_id = message.chat.id
    #     return user_id in self.admins[chat_id]

