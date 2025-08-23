import logging
import os

from resources.values import log_file_name

os.makedirs("logs", exist_ok=True)


def create_local_logger():
    return logging.getLogger(__name__)


def setup_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(
        os.path.join("logs", log_file_name), encoding="utf-8"
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s |%(message)s")
    )
    root_logger.addHandler(file_handler)
