import logging
import os
import time

class PackagePathFilter(logging.Filter):
    def filter(self, record):
        record.pathname = record.pathname.replace(os.getcwd(),"")
        return True

def initialize_logger(str):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    f_handler = logging.FileHandler(filename=str, mode="a")
    f_handler.setLevel(logging.INFO)
    f_handler.addFilter(PackagePathFilter())
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_handler.addFilter(PackagePathFilter())
    format = logging.Formatter(
        fmt='%(asctime)s :: [%(levelname)-s] ::  [%(pathname)s %(funcName)s %(lineno)d] :: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    format.converter = time.gmtime
    f_handler.setFormatter(format)
    c_handler.setFormatter(format)
    logger.addHandler(f_handler)
    logger.addHandler(c_handler)
    return logger
