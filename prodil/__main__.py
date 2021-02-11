# from prodil.models.model import Documents, Links, Books, Questions
from prodil.BotConfig import ProDil

# import configparser
# import logging

# from decouple import config

# logging.basicConfig(
#     format="%(levelname)s - %(name)s - %(message)s",
#     level=logging.getLevelName(config("LOG_LEVEL", default="INFO")),
# )

if __name__ == "__main__":
    ProDil().run()
