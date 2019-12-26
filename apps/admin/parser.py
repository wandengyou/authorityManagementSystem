from flask_restful import reqparse, inputs

base = reqparse.RequestParser(bundle_errors=True)

paginate = base.copy()
paginate.add_argument('page_size', type=inputs.positive, required=True)
paginate.add_argument('page_num', type=inputs.positive, required=True)

platform = base.copy()
platform.add_argument('name', type=str, required=True)
platform.add_argument('code', type=str, required=True)
platform.add_argument('description', type=str, store_missing=False)

platform_query = paginate.copy()
platform_query.add_argument('name', type=str, store_missing=False)
platform_query.add_argument('code', type=str, store_missing=False)

role = base.copy()
role.add_argument('platform_code', type=str, required=True)
role.add_argument('role_name', type=str, required=True)
role.add_argument('role_code', type=str, required=True)
role.add_argument('description', type=str, store_missing=False)

role_query = paginate.copy()
role_query.add_argument('platform_code', type=str, store_missing=False)

menu = base.copy()
menu.add_argument('platform_code', type=str, required=True)
menu.add_argument('menu_name', type=str, required=True)
menu.add_argument('menu_code', type=str, required=True)
menu.add_argument('menu_level', type=inputs.positive, required=True)
menu.add_argument('sequence', type=inputs.positive, required=True)
menu.add_argument('parent_id', type=inputs.positive, store_missing=False)
menu.add_argument('description', type=str, store_missing=False)

menu_handle = base.copy()
menu_handle.add_argument('platform_code', type=str, required=True)
menu_handle.add_argument('menu_id', type=inputs.positive, required=True)
menu_handle.add_argument('handle_name', type=str, required=True)
menu_handle.add_argument('handle_code', type=str, required=True)
menu_handle.add_argument('api_host', type=str, required=True)
menu_handle.add_argument('api_path', type=str, required=True)
menu_handle.add_argument('api_params', type=str, required=True)
menu_handle.add_argument('api_md5', type=str, store_missing=False)
menu_handle.add_argument('remarks', type=str, store_missing=False)

role_menu = base.copy()
role_menu.add_argument('role_id', type=inputs.positive, required=True)
role_menu.add_argument('handle_id', type=inputs.positive, required=True)

role_menu_search = paginate.copy()
role_menu_search.add_argument('role_id', type=inputs.positive, required=True)

user_role = base.copy()
user_role.add_argument('user_code', type=str, required=True)
user_role.add_argument('platform_code', type=str, required=True)
user_role.add_argument('role_id', type=inputs.positive, required=True)

user_role_search = paginate.copy()
user_role_search.add_argument('user_code', type=str, store_missing=False)

user_permission = base.copy()
user_permission.add_argument('user_code', type=str, required=True)

check_permission = base.copy()
check_permission.add_argument('user_code', type=str, required=True)
check_permission.add_argument('handle_code', type=str, required=True)
