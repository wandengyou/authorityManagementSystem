from flask import Blueprint
from flask_restful import Api

bp = Blueprint('admin', __name__)
api = Api(bp, prefix='/admin')

from . import urls  # noqa
