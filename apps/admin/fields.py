from flask_restful import fields

platform_response = {
    'id': fields.Integer,
    'platform_name': fields.String,
    'platform_code': fields.String,
    'status': fields.String,
    'description': fields.String
}

role_response = {
    'id': fields.Integer,
    'platform_code': fields.String,
    'role_name': fields.String,
    'role_code': fields.String,
    'description': fields.String,
}

menu_response = {
    'id': fields.Integer,
    'platform_code': fields.String,
    'menu_name': fields.String,
    'menu_code': fields.String,
    'sequence': fields.Integer,
    'parent_id': fields.Integer,
    'menu_level': fields.Integer,
}

menu_handle_response = {
    'id': fields.Integer,
    'platform_code': fields.String,
    'menu_id': fields.Integer,
    'handle_name': fields.String,
    'handle_code': fields.String,
    'api_path': fields.String,
    'api_host': fields.String,
    'api_params': fields.String,
    'api_md5': fields.String,
    'api_remarks': fields.String,
}

role_handle_id_response = {
    'role_id': fields.Integer,
    'handle_id': fields.Integer,
}

role_handle_response = {
    'id': fields.Integer,
    'role_id': fields.Integer,
    'handle': fields.Nested(menu_handle_response)
}

user_role_response = {
    'id': fields.Integer,
    'user_code': fields.String,
    'role': fields.Nested(role_response)
}