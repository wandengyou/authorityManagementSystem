from pymaid.conf import settings

try:
    from .local import *  # noqa
except ImportError as ex:
    print(ex)

from . import crypto
from . import flask
from . import log
from . import server
from . import storage

settings.load_from_object(crypto)
settings.load_from_object(flask)
settings.load_from_object(log)
settings.load_from_object(server)
settings.load_from_object(storage)
