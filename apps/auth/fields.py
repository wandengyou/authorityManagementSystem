from flask_restful import fields

platform_response = {
    'id': fields.Integer,
    'platform_name': fields.String,
    'platform_code': fields.String,
    'status': fields.String,
    'description': fields.String,
    'permission_total': fields.Integer,
    'role_total': fields.Integer,
    'user_total': fields.Integer
}

role_response = {
    'id': fields.Integer,
    'role_name': fields.String,
    'role_code': fields.String,
    'permission_total': fields.Integer,
    'description': fields.String,
}

permission_response = {
    'id': fields.Integer,
    'platform_code': fields.String,
    'permission_name': fields.String,
    'permission_code': fields.String,
    'permission_type': fields.Integer,
    'identifier': fields.String,
}

