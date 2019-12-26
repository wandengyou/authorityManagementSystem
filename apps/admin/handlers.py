from core.ext import ModelManager
from core.utils import id_model_map

from .models import Platform, Role, Menu, MenuHandle, RoleHandle, UserRole
from .error import CommonError


def query_platform(page_size, page_num):
    platform_manager = ModelManager(
        Platform,
        page_size=page_size,
        page_num=page_num,
    )
    return platform_manager.paginate()


def add_platform(name, code, **kwargs):
    platform = Platform(
        platform_name=name,
        platform_code=code,
        status=Platform.Status.USED.value,
        description=kwargs.get('description', None)
    )
    return ModelManager(platform).save()


def add_role(platform_code, role_name, role_code, **kwargs):
    role = Role(
        platform_code=platform_code,
        role_code=role_code,
        role_name=role_name,
        description=kwargs.get('description', None)
    )
    return ModelManager(role).save()


def query_role(page_num, page_size, **kwargs):
    role_manager = ModelManager(
        Role,
        page_size=page_size,
        page_num=page_num,
        filters=kwargs
    )
    return role_manager.paginate()


def query_menu(page_size, page_num):
    menu_manager = ModelManager(Menu, page_size=page_size, page_num=page_num)
    return menu_manager.paginate()


def add_menu(platform_code, menu_name, menu_code,  sequence=1, parent_id=0, menu_level=1):
    menu = Menu(
        platform_code=platform_code,
        menu_name=menu_name,
        menu_code=menu_code,
        sequence=sequence,
        parent_id=parent_id,
        menu_level=menu_level,
    )
    return ModelManager(menu).save()


def query_menu_interface(page_size, page_num):
    interface_manager = ModelManager(MenuHandle, page_size=page_size, page_num=page_num)
    return interface_manager.paginate()


def add_menu_interface(platform_code, menu_id, handle_name, handle_code,
                       api_path, api_host, api_params, api_md5, **kwargs):
    menu_handle = MenuHandle(
        platform_code=platform_code,
        menu_id=menu_id,
        handle_name=handle_name,
        handle_code=handle_code,
        api_path=api_path,
        api_host=api_host,
        api_params=api_params,
        api_md5=api_md5,
        api_remarks=kwargs.get('remarks', None)
    )
    return ModelManager(menu_handle).save()


def add_role_menu_interface(role_id, handle_id):
    role = ModelManager(Role).query_by_id(role_id)
    if not role:
        raise CommonError.NotExist(data={'role_id': role_id})
    handle = ModelManager(MenuHandle).query_by_id(handle_id)
    if not handle:
        raise CommonError.NotExist(data={'handle_id': handle_id})
    role_handle = RoleHandle(role=role, handle=handle)
    return ModelManager(role_handle).save()


def query_role_menu_interface(role_id, page_size, page_num):
    handle_manager = ModelManager(
        RoleHandle,
        page_size=page_size,
        page_num=page_num,
        filters={'role_id': role_id},
        serialize=False
    )
    return handle_manager.paginate()


def add_user_role(platform_code, user_code, role_id):
    role = ModelManager(Role).query_by_id(role_id)
    if not role:
        raise CommonError.NotExist(data={'role_id': role_id})

    user_role = UserRole(
        platform_code=platform_code,
        user_code=user_code,
        role=role
    )
    return ModelManager(user_role).save()


def query_user_role(user_code, page_size, page_num):
    ur_manager = ModelManager(
        UserRole,
        page_size=page_size,
        page_num=page_num,
        filters={'user_code': user_code},
        serialize=False
    )
    return ur_manager.paginate()


def get_user_permissions(user_code):
    user = ModelManager(UserRole).query_one_by_filter(user_code=user_code)
    if not user:
        raise CommonError.NotExist(data={'user_code': user_code})
    role_handles = ModelManager(RoleHandle).query(role_id=user.role_id)
    if role_handles:
        handles = [handle.handle for handle in role_handles]
        menus = ModelManager(Menu).query(platform_code=user.platform_code)
        platform_menu_map = id_model_map(menus)
        first_menu_ids, second_menu_ids, three_menu_ids = set(), set(), set()
        for handle in handles:
            order = handle.catalog.split('/')
            first_menu_ids.add(int(order[0]))
            second_menu_ids.add(int(order[1]))
            if len(order) > 2:
                three_menu_ids.add(int(order[2]))
        first_menu = [platform_menu_map[menu_id].to_dict() for menu_id in first_menu_ids]
        second_menu = [platform_menu_map[menu_id].to_dict() for menu_id in second_menu_ids]
        three_menu = [platform_menu_map[menu_id].to_dict() for menu_id in three_menu_ids]
        return permission_tree(first_menu, second_menu, three_menu, handles)
    else:
        return []


def get_platform_permissions(platform_code):
    platform_menus = ModelManager(Menu).query(platform_code=platform_code)
    handles = ModelManager(MenuHandle).query(platform_code=platform_code)
    first_menu, second_menu, three_menu = [], [], []
    for menu in platform_menus:
        if menu.menu_level == 1:
            first_menu.append(menu.to_dict())
        elif menu.menu_level == 2:
            second_menu.append(menu.to_dict())
        else:
            three_menu.append(menu.to_dict())
    return permission_tree(first_menu, second_menu, three_menu, handles)


def permission_tree(first_menu, second_menu, three_menu, handles):

    def add_child_permission(parent_menu, child_menus):
        parent_child_menus = [
            child
            for child in child_menus
            if parent_menu['id'] == child['parent_id']
        ]
        parent_menu['child_permission'] = parent_child_menus
        return parent_menu

    def add_menu_handle(menu):
        menu['child_permission'] = [
            handle.to_dict()
            for handle in handles
            if menu['id'] == handle.menu_id
        ]
        return menu
    if three_menu:
        [add_menu_handle(menu) for menu in three_menu]
        second_menu = [add_child_permission(second, three_menu) for second in second_menu]
    [add_menu_handle(menu) for menu in second_menu]
    [add_child_permission(first, second_menu) for first in first_menu]
    return first_menu


def check_permission(user_code, handle_code):
    user = ModelManager(UserRole).query_one_by_filter(user_code=user_code)
    if not user:
        raise CommonError.NotExist(data={'user_code': user_code})
    handles = ModelManager(RoleHandle).query(role_id=user.role_id)
    user_handle_codes = [handle.handle.handle_code for handle in handles]
    return True if handle_code in user_handle_codes else False
