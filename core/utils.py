from functools import wraps
from hashlib import md5
from time import time

from flask import request
from six import text_type

from pymaid.conf import settings


def get_auth_code(data, key):
    return md5(
        (key + md5(data.encode('utf8')).hexdigest()).encode('utf-8')
    ).hexdigest()


# def with_lock(lock_name, key_name=None, timeout=10, blocking_timeout=10):
#
#     def wrapper(func):
#         @wraps(func)
#         def _(*args, **kwargs):
#             assert args or key_name in kwargs
#             key = lock_name.format(args and args[0] or kwargs[key_name])
#             with get_cache_redis().lock(
#                     key, timeout, blocking_timeout=blocking_timeout):
#                 return func(*args, **kwargs)
#         return _
#     return wrapper


if settings.get('DEBUG', ns='server') and settings.get('TEST', ns='server'):
    def validate_auth_code(auth_code, req, secret):
        return True

    def validate_expiration(timestamp, interval):
        return True
else:
    def validate_auth_code(auth_code, req, secret):
        data = u'_'.join(
            text_type(req[key]) for key in sorted(req) if req[key] is not None
        )
        sign = md5(
            (secret + md5(data.encode('utf8')).hexdigest().encode('utf-8'))
        ).hexdigest()
        return auth_code == sign

    def validate_expiration(timestamp, interval):
        return abs(time() * 1000 - timestamp) <= interval


def get_platform():
    platform = request.user_agent.platform.lower()
    if platform == 'android':
        return 'android'
    if platform in ('iphone', 'ipad', 'ipod'):
        return 'iOS'
    return 'other'


def get_ip():
    ip = request.headers.get('X-Forwarded-For') or request.remote_addr
    return ip.split(',')[0]


def id_model_map(models, key=None):
    model_dict = {}

    def get_result(model):
        if key:
            if hasattr(model, key) and (getattr(model, key) not in model_dict):
                model_dict[getattr(model, key)] = model
        else:
            if model.id not in model_dict:
                model_dict[model.id] = model
        return model_dict

    list(map(get_result, models))
    return model_dict
