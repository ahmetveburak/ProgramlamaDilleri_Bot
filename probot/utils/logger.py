import logging
from os import makedirs
from os.path import exists, join


def get_logger(
    name=None, file_name="prodil.log", level=logging.WARNING, log_dir="logs"
):
    if not exists(log_dir):
        makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(join(log_dir, file_name))
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    fh.setLevel(level)
    logger.addHandler(fh)

    return logger
