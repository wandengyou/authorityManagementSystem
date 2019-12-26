# -*- coding: utf-8 -*-
import json
import re
import importlib
import pymaid

from hashlib import md5
from pymaid.conf import settings
from pymaid.error import ErrorManager

from flask import Flask, jsonify, request
from flask_cors import CORS

from core.ext import db


CommonError = ErrorManager.create_manager('CommonError', 1000)
CommonError.add_error('AuthFailed', 1, 'interface authentication failed')


def create_app(apps):
    app = Flask(__name__)
    app.config.from_mapping(settings.namespaces['flask'])
    app.config.from_mapping(settings.namespaces['storage'])

    configure_blueprints(app, apps)
    configure_extensions(app)
    configure_errorhandlers(app)
    response_handler(app)
    # request_handler(app)

    return app


def request_handler(app):
    @app.before_request
    def verify_request():
        request_params = request.values.to_dict()
        request_sign = request_params.pop('sign', None)
        request_params['AccessKey'] = 'access'
        request_params['SecretKey'] = 'secret'
        sorted_params = {}
        for key in sorted(request_params.keys()):
            sorted_params[key] = request_params[key]
        auth_sign = ''
        for key, value in sorted_params.items():
            auth_sign += (key + '=' + value + '&')
        sign = md5(auth_sign[0:len(auth_sign)-1].encode('utf8')).hexdigest().upper()
        if sign != request_sign:
            raise CommonError.AuthFailed(data={'url': request.url})
        # use redis record timeout


def response_handler(app):
    @app.after_request
    def response(res):
        if res.status_code // 100 == 2:
            try:
                res_json = json.loads(res.response[0])
                if 'code' in res_json:
                    res_data = res_json
                else:
                    res_data = {'code': 200, 'data': res_json}
                res.response[0] = json.dumps(res_data)
                res.content_length = len(res.response[0])
            except Exception:
                return res
        return res


def configure_blueprints(app, apps):
    for name in apps:
        mod = importlib.import_module(name)
        if hasattr(mod, 'bp'):
            try:
                importlib.import_module(name + '.urls')
            except ImportError as ex:
                if re.match(r'No module named .*\.urls', str(ex)):
                    continue
                raise
            app.register_blueprint(mod.bp)


def configure_extensions(app):

    # @login_manager.user_loader
    # def load_user(user_id):
    #     """Loads the user. Required by the `login` extension."""
    #     return None
    #     # return SessionUser(user_id)
    # login_manager.init_app(app)
    # login_manager.anonymous_user = AnonymousUser
    #
    db.init_app(app)
    # # app.session_interface = session_interface
    # limiter.init_app(app)
    CORS(app, supports_credentials=True)


def configure_errorhandlers(app):
    @app.errorhandler(pymaid.error.BaseEx)
    def custom_error(error):
        return jsonify(
            {'code': error.code, 'message': error.message, 'data': error.data},
        ), 400
