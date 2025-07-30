import logging

logging_logger = logging.getLogger(__name__)
logging_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging_logger.addHandler(handler)
