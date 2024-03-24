import json
import logging
import logging.config
import os

from dotenv import load_dotenv

load_dotenv()

logging_config_path = os.getenv("LOG_CONFIG")


def configure_logging():
    with open(logging_config_path, "rt") as f:
        config = json.load(f)
    logging.config.dictConfig(config)
