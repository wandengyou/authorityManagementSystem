from . import api
from . import restful


api.add_resource(restful.PlatformManager, '/platform/')
api.add_resource(restful.RoleManager, '/role/')
api.add_resource(restful.UserManager, '/user/')
api.add_resource(restful.PermissionManager, '/permission/')
api.add_resource(restful.RolePermissionManager, '/assign_permission/')
api.add_resource(
    restful.AssignRole, 
    '/assign_role/<string:user_code>/<string:role_code>/'
)
api.add_resource(
    restful.CheckPermission,
    '/authenticate/<string:user_code>/<string:permission_code>/'
)
api.add_resource(restful.UserPermission, '/permission/<string:user_code>/')
api.add_resource(restful.UserRole, '/role/<string:user_code>/')
api.add_resource(restful.PlatFormPermission, '/platform/<string:platform_code>/')
