import mongoengine

# from mongoengine import document
from prodil.models.model import Documents, Links, Books, Questions
from prodil.BotConfig import ProDil
import logging
from decouple import config

# logging.basicConfig(
#     format="%(levelname)s - %(name)s - %(message)s",
#     level=logging.getLevelName(config("LOG_LEVEL", default="INFO")),
# )


mongoengine.register_connection(alias="core", name="prodil_test")


# path = os.getcwd()
if __name__ == "__main__":
    ProDil().run()
