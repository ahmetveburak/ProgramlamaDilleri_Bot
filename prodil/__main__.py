import logging
from os import makedirs
from os.path import join

from prodil.BotConfig import ProDil

log_dir = "logs"
try:
    makedirs(log_dir)
except FileExistsError:
    pass

logger = logging.getLogger()
fh = logging.FileHandler(join(log_dir, "prodil.log"))
fh.setLevel(logging.NOTSET)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


if __name__ == "__main__":
    ProDil().run()
