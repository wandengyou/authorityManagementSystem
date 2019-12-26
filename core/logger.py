import sys
import logging
import logging.config

from time import time
from functools import wraps

from flask import request
from flask.views import MethodView
from flask_login import current_user

from core.utils import get_ip

if sys.version_info.major >= 3:
    logging_levels = logging._levelToName
    logging_names = logging._nameToLevel
else:
    logging_names = logging_levels = logging._levelNames


# create logger
project_logger = logging.getLogger('distributor-api')


def class_logger(cls):
    cls.logger = project_logger.getChild(cls.__name__)
    return cls


def update_record(record, level, msg, *args):
    record.levelno = level
    record.levelname = logging_levels[level]
    record.msg = msg
    record.args = args
    ct = time()
    record.created = ct
    record.msecs = (ct - int(ct)) * 1000


def trace_view(level=logging.INFO):
    def wrapper(view):
        for method in view.methods:
            method = method.lower()
            setattr(view, method, trace_method(level)(getattr(view, method)))
        return view
    if isinstance(level, str):
        level = logging_names[level]
        return wrapper
    elif isinstance(level, int):
        return wrapper
    else:
        assert issubclass(level, MethodView), level
        view, level = level, logging.INFO
        return wrapper(view)


def trace_method(level=logging.INFO):
    def wrapper(func):
        assert level in logging_levels, (level, logging_levels)
        co = func.__code__
        # name, level, fn, lno, msg, args, exc_info, func
        record = logging.LogRecord(
            '', level, co.co_filename, co.co_firstlineno, '', (), None,
            co.co_name
        )

        @wraps(func)
        def _(self, *args, **kwargs):
            data = {}
            if request.args:
                data['args'] = request.args
            if request.form:
                data['form'] = request.form
            if request.get_json():
                data['json'] = request.get_json()
            peer = get_ip()
            user = current_user

            try:
                resp = func(self, *args, **kwargs)
            except BaseException as ex:
                update_record(
                    record, logging.ERROR,
                    u'[%s@%s][%s|%s] [request|%.255r] [exception|%.255r]',
                    user, peer, request.method, request.path, data, ex
                )
                self.logger.handle(record)
                raise

            update_record(
                record, level,
                u'[%s@%s][%s|%s] [request|%.255r] [response|%.255r]',
                user, peer, request.method, request.path, data, resp
            )
            # self.logger.handle(record)
            return resp
        return _
    if isinstance(level, str):
        level = logging_names[level]
        return wrapper
    elif isinstance(level, int):
        return wrapper
    else:
        assert callable(level)
        func, level = level, logging.INFO
        return wrapper(func)
