from . import api
from . import restful


api.add_resource(restful.PlatformManager, '/platform')
api.add_resource(restful.RoleManager, '/role')
api.add_resource(restful.MenuManager, '/menu')
api.add_resource(restful.MenuHandleManager, '/menu_handle')
api.add_resource(restful.RoleMenuManager, '/role_menu')
api.add_resource(restful.UserRoleManager, '/user_role')

api.add_resource(restful.CheckPermission, '/check_permission')
api.add_resource(restful.UserPermission, '/permission/<string:user_code>')
api.add_resource(restful.PlatFormPermission, '/platform/<string:platform_code>')
