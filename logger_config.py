import logging
import logging.config

def log(file_name):
    log_name = str(file_name) + '_log.log'
    logging.basicConfig(filename = log_name, level = logging.DEBUG, filemode = 'w')

