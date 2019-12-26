from flask_restful import reqparse, inputs

base = reqparse.RequestParser(bundle_errors=True)

paginate = base.copy()
paginate.add_argument('page_size', type=inputs.positive, store_missing=False)
paginate.add_argument('page_num', type=inputs.positive, store_missing=False)

platform = base.copy()
platform.add_argument('name', type=str, required=True)
platform.add_argument('host', type=str, required=True)
platform.add_argument('description', type=str, store_missing=False)

platform_query = paginate.copy()
platform_query.add_argument('platform_name', type=str, store_missing=False)
platform_query.add_argument('status', type=str, store_missing=False)

user = base.copy()
user.add_argument('user_code', type=str, required=True)
user.add_argument('platform_code', type=str, required=True)

user_query = paginate.copy()
user_query.add_argument('platform_code', type=str, store_missing=False)
user_query.add_argument('user_code', type=str, store_missing=False)


role = base.copy()
role.add_argument('platform_code', type=str, required=True)
role.add_argument('role_name', type=str, required=True)
role.add_argument('description', type=str, store_missing=False)

role_query = paginate.copy()
role_query.add_argument('platform_code', type=str, store_missing=False)
role_query.add_argument('role_name', type=str, store_missing=False)

permission = base.copy()
permission.add_argument('platform_code', type=str, required=True)
permission.add_argument('permission_name', type=str, required=True)
permission.add_argument('permission_type', type=str, required=True)

permission_query = paginate.copy()
permission_query.add_argument('platform_code', type=str, store_missing=False)
permission_query.add_argument('permission_name', type=str, store_missing=False)
permission_query.add_argument('permission_code', type=str, store_missing=False)
permission_query.add_argument('permission_type', type=str, store_missing=False)


role_permission = base.copy()
role_permission.add_argument('role_id', type=inputs.positive, required=True)
role_permission.add_argument('permission_id', type=str, required=True)

role_permission_query = paginate.copy()
role_permission_query.add_argument('role_id', type=inputs.positive,
                                  store_missing=False)

user_role = base.copy()
user_role.add_argument('user_code', type=str, required=True)
user_role.add_argument('role_id', type=inputs.positive, required=True)

user_role_query = paginate.copy()
user_role_query.add_argument('user_code', type=str, store_missing=False)

user_permission = base.copy()
user_permission.add_argument('user_code', type=str, required=True)

check_permission = base.copy()
check_permission.add_argument('user_code', type=str, required=True)
check_permission.add_argument('permission_code', type=str, required=True)


