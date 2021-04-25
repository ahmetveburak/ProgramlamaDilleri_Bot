from prodil.BotConfig import ProDil
from decouple import config
import logging

# RUNTIME DEBUG LOG_LEVEL INFO
logging.basicConfig(
    format="%(levelname)s - %(name)s - %(message)s",
    level=logging.getLevelName(config("LOG_LEVEL", default="ERROR")),
)

if __name__ == "__main__":
    ProDil().run()
