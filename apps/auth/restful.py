import pandas as pd
from flask import request
from flask.views import MethodView
from flask_restful import marshal

from core.logger import class_logger, trace_view

from .models import Platform
from . import handlers
from . import parser
from . import fields


@trace_view
@class_logger
class AssignRole(MethodView):

    def post(self, user_code, role_code):
        flag = handlers.add_user_role(user_code, role_code)
        return {'status': flag}

    def delete(self, user_code, role_code):
        flag = handlers.remove_user_role(user_code, role_code)
        return {'status': flag}


@trace_view
@class_logger
class UserRole(MethodView):

    def get(self, user_code):
        roles, total = handlers.get_user_role(user_code)
        return {'data': roles, 'total': total}



@trace_view
@class_logger
class PlatformManager(MethodView):

    parse_get = parser.platform_query
    parse_post = parser.platform
    parse_put = parser.platform_handle
    parse_del = parser.platform_handle

    def get(self):
        req_dict = self.parse_get.parse_args()
        platforms, total = handlers.query_platform(**req_dict)
        return {
            'data': marshal(platforms, fields.platform_response),
            'total': total,
        }

    def post(self):
        req_dict = self.parse_post.parse_args()
        platform = handlers.add_platform(**req_dict)
        return marshal(platform, fields.platform_response)

    def put(self):
        req_dict = self.parse_put.parse_args()
        flag = handlers.platform_handle(
            status=Platform.Status.USED.value,
            **req_dict
        )
        return {'status': flag}

    def delete(self):
        req_dict = self.parse_put.parse_args()
        flag = handlers.platform_handle(
            req_dict['platform_code'], 
            Platform.Status.FORBIDDEN.value
        )
        return {'status': flag}


@trace_view
@class_logger
class RoleManager(MethodView):

    parse_get = parser.role_query
    parse_post = parser.role
    parse_put = parser.role_update

    def get(self):
        req_dict = self.parse_get.parse_args()
        roles, total = handlers.query_role(**req_dict)
        return {
            'data': marshal(roles, fields.role_response),
            'total': total
        }

    def post(self):
        req_dict = self.parse_post.parse_args()
        role = handlers.add_role(**req_dict)
        return marshal(role, fields.role_response)

    def put(self):
        req_dict = self.parse_put.parse_args()
        flag = handlers.update_role(**req_dict)
        return {'status': flag}



@trace_view
@class_logger
class PermissionManager(MethodView):

    parse_get = parser.permission_query
    parse_post = parser.permission
    parse_put = parser.permission_update
    
    def get(self):
        req_dict = self.parse_get.parse_args()
        permissions, total = handlers.query_permission(**req_dict)
        return {
            'data': marshal(permissions, fields.permission_response),
            'total': total
        }

    def post(self):
        req_dict = self.parse_post.parse_args()
        permission = handlers.add_permission(**req_dict)
        return marshal(permission, fields.permission_response)
    
    def put(self):
        req_dict = self.parse_put.parse_args()
        print(req_dict)
        flag = handlers.update_permission(**req_dict)
        return {'status': flag}


@trace_view
@class_logger
class UserManager(MethodView):

    parse_get = parser.user_query
    parse_post = parser.user

    def get(self):
        req_dict = self.parse_get.parse_args()
        users, total = handlers.query_user(**req_dict)
        return {
            'data': users,
            'total': total
        }

    def post(self):
        req_dict = self.parse_post.parse_args()
        handlers.register(**req_dict)
        return {'status': 'successful user registration'}


@trace_view
@class_logger
class RolePermissionManager(MethodView):

    parse_get = parser.role_permission_query
    parse_post = parser.role_permission

    def get(self):
        req_dict = self.parse_get.parse_args()
        role_permissions, total = handlers.query_role_permissions(**req_dict)
        permissions = []
        if total > 0:
            permissions = [rp.permission for rp in role_permissions]
        return {
            'data': marshal(permissions, fields.permission_response),
            'total': total
        }

    def post(self):
        req_dict = self.parse_post.parse_args()
        flag = handlers.add_role_permissions(**req_dict)
        return {'status': flag}

    def delete(self):
        req_dict = self.parse_post.parse_args()
        flag = handlers.remove_role_permissions(**req_dict)
        return {'status': flag}
        



@trace_view
@class_logger
class UserPermission(MethodView):

    def get(self, user_code):
        permissions, total = handlers.get_user_permissions(user_code)
        return {
            'data': marshal(permissions, fields.permission_response),
            'total': total
        }


@trace_view
@class_logger
class CheckPermission(MethodView):

    parse_get = parser.check_permission

    def get(self, user_code, permission_code):
        flag = handlers.check_permission(user_code, permission_code)
        return {'status': flag}


@trace_view
@class_logger
class PlatFormPermission(MethodView):

    def get(self, platform_code):
        permissions =  handlers.get_platform_permissions(platform_code)
        return marshal(permissions, fields.permission_response)


@trace_view
@class_logger
class ImportPermission(MethodView):

    parse_post = parser.data_import

    def post(self, platform_code):
        req_dict = self.parse_post.parse_args()
        file = request.files['file']
        permissions = handlers.import_permission(
            platform_code, file, **req_dict
        )
        return {
            'data': marshal(permissions, fields.permission_response),
            'total': len(permissions)
        }
       
