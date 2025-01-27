import colorlog
import logging


def setup_logging(save=False):
    console_handler = colorlog.StreamHandler()

    log_format = "%(asctime)s | %(name)s - %(levelname)s: %(message)s"
    formatter = colorlog.ColoredFormatter("%(log_color)s" + log_format)
    console_handler.setFormatter(formatter)


    logger = logging.getLogger("root")
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    
    if save:
        file_handler = logging.FileHandler('app.log', mode='w')
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name):
    return logging.getLogger(name)