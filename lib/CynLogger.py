"""
    Logging facility

    Logging Levels
    -------------------------
    | Level     | Num value
    -------------------------
    | CRITICAL  | 50
    | ERROR     | 40
    | WARNING   | 30
    | INFO      | 20
    | DEBUG     | 10
    | NOTSET    |  0
    -------------------------

    Python Version: 3.x
"""

__autor__       = "Yannic Schneider"
__copyright__   = "Copyright 2017"
__version__     = "1.0"
__email__       = "v@vendetta.ch"
__status__      = "Productive"
__docformat__   = "reStructuredText"


################################################################################
# CODE
################################################################################

import os
import json
import logging
from logging.config import dictConfig

################################################################################

def setup_logging(config = None, app_name = 'DEFAULT'):
    """Setup logging configuration

    """
    isDefault = False
    
    if config == None:
        # Load default
        isDefault = True
        config = load_default()

    logging.config.dictConfig(config)

    # Get logger instance
    log = logging.getLogger(app_name + __name__)
    log.info('#### EXECUTION STARTED ####')
    if isDefault:
    	log.info('Default Logger configuration successful loaded.')
    log.info('User Logger configuration successful loaded.')

def load_default():
    return json.loads("""
    {
        "version": 1,
        "disable_existing_loggers": false,
        "formatters": {
            "simple": {
                "class": "logging.Formatter",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "%(asctime)s:%(name)s:%(levelname)s:%(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "/home/cyn/code/CynCrypto/var/info.log",
                "maxBytes": 1048576,
                "backupCount": 20,
                "encoding": "utf8"
            },
            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": "/home/cyn/code/CynCrypto/var/errors.log",
                "maxBytes": 1048576,
                "backupCount": 20,
                "encoding": "utf8"
            }
        },
        "loggers": {
            "my_module": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": "no"
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": [
                "console", 
                "info_file_handler", 
                "error_file_handler"]
        }
    }
    """)
################################################################################
