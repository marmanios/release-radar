# logger.py 

import logging
import os
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(console_handler)

    return logger