__NAMESPACE__ = 'logging'

from core import g

LOGGING = {
    'handlers': {
        'console': {
            'level': 'WARN',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': g.ROOT_PATH / 'logs/app.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'distributor-api': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'pymaid': {
            'handlers': ['console', 'file'],
        },
    }
}
