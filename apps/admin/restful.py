from flask.views import MethodView
from flask_restful import marshal

from core.logger import class_logger, trace_view

from . import handlers
from . import parser
from . import fields


@trace_view
@class_logger
class UserRoleManager(MethodView):

    parse_get = parser.user_role_search
    parse_post = parser.user_role

    def get(self):
        req_dict = self.parse_get.parse_args()
        user_roles, total = handlers.query_user_role(**req_dict)
        return {
            'data': marshal(user_roles, fields.user_role_response),
            'total': total
        }

    def post(self):
        req_dict = self.parse_post.parse_args()
        user_role = handlers.add_user_role(**req_dict)
        return marshal(user_role, fields.user_role_response)


@trace_view
@class_logger
class PlatformManager(MethodView):

    parse_get = parser.platform_query
    parse_post = parser.platform

    def get(self):
        req_dict = self.parse_get.parse_args()
        platforms, total = handlers.query_platform(**req_dict)
        return {
            'data': marshal(platforms, fields.platform_response),
            'total': total
        }

    def post(self):
        req_dict = self.parse_post.parse_args()
        platform = handlers.add_platform(**req_dict)
        return marshal(platform, fields.platform_response)


@trace_view
@class_logger
class RoleManager(MethodView):

    parse_get = parser.role_query
    parse_post = parser.role

    def get(self):
        req_dict = self.parse_get.parse_args()
        roles, total = handlers.query_role(
            page_num=req_dict.pop('page_num'),
            page_size=req_dict.pop('page_size'),
            **req_dict
        )
        return {
            'data': marshal(roles, fields.role_response),
            'total': total
        }

    def post(self):
        req_dict = self.parse_post.parse_args()
        role = handlers.add_role(**req_dict)
        return marshal(role, fields.role_response)


@trace_view
@class_logger
class MenuManager(MethodView):

    parse_get = parser.paginate
    parse_post = parser.menu

    def get(self):
        req_dict = self.parse_get.parse_args()
        menus, total = handlers.query_menu(**req_dict)
        return {
            'data': marshal(menus, fields.menu_response),
            'total': total
        }

    def post(self):
        req_dict = self.parse_post.parse_args()
        menu = handlers.add_menu(**req_dict)
        return marshal(menu, fields.menu_response)


@trace_view
@class_logger
class MenuHandleManager(MethodView):

    parse_get = parser.paginate
    parse_post = parser.menu_handle

    def get(self):
        req_dict = self.parse_get.parse_args()
        menu_interfaces, total = handlers.query_menu_interface(**req_dict)
        return {
            'data': marshal(menu_interfaces, fields.menu_handle_response),
            'total': total
        }

    def post(self):
        req_dict = self.parse_post.parse_args()
        menu_handle = handlers.add_menu_interface(**req_dict)
        return marshal(menu_handle, fields.menu_handle_response)


@trace_view
@class_logger
class RoleMenuManager(MethodView):

    parse_get = parser.role_menu_search
    parse_post = parser.role_menu

    def get(self):
        req_dict = self.parse_get.parse_args()
        menu_interfaces, total = handlers.query_role_menu_interface(**req_dict)
        return {
            'data': marshal(menu_interfaces, fields.role_handle_response),
            'total': total
        }

    def post(self):
        req_dict = self.parse_post.parse_args()
        role_handle = handlers.add_role_menu_interface(**req_dict)
        return marshal(role_handle, fields.role_handle_id_response)


@trace_view
@class_logger
class UserPermission(MethodView):

    def get(self, user_code):
        return handlers.get_user_permissions(user_code)


@trace_view
@class_logger
class CheckPermission(MethodView):

    parse_get = parser.check_permission

    def get(self):
        req_dict = self.parse_get.parse_args()
        flag = handlers.check_permission(**req_dict)
        return {'status': flag}


@trace_view
@class_logger
class PlatFormPermission(MethodView):

    def get(self, platform_code):
        return handlers.get_platform_permissions(platform_code)

