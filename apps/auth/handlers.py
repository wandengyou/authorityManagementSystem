from core.ext import ModelManager, db
from core.utils import id_model_map

from .models import *
from .error import CommonError


def register(platform_code, user_code):
    user = User(
        platform_code=platform_code,
        user_code=user_code
    )
    ModelManager(user).save()


def query_user(page_size=15, page_num=1, **kwargs):
    user_manager = ModelManager(
        User,
        page_size=page_size,
        page_num=page_num
    )
    if kwargs:
        user_manager.filters = kwargs
    return user_manager.paginate()


def query_platform(page_size=15, page_num=1, **kwargs):
    platform_manager = ModelManager(
        Platform,
        page_size=page_size,
        page_num=page_num
    )
    if kwargs:
        platform_manager.filters = kwargs
    return platform_manager.paginate()


def add_platform(name, host, **kwargs):
    platform = Platform(
        platform_name=name,
        platform_host=host,

    )
    if kwargs:
        for key, value in kwargs.items():
            setattr(platform, key, value)
    return ModelManager(platform).save()


def add_role(platform_code, role_name, description=None):
    role = Role(
        platform_code=platform_code,
        role_name=role_name,
        description=description
    )
    return ModelManager(role).save()


def query_role(page_num=1, page_size=15, **kwargs):
    role_manager = ModelManager(
        Role,
        page_size=page_size,
        page_num=page_num,
    )
    if kwargs:
        role_manager.filters = kwargs
    return role_manager.paginate()


def query_permission(page_num=1, page_size=15, **kwargs):
    print(kwargs)
    permission_manager = ModelManager(
        Permission, 
        page_size=page_size, 
        page_num=page_num
    )
    if kwargs:
        permission_manager.filters = kwargs
    return permission_manager.paginate()


def add_permission(platform_code, permission_name, permission_type):
    permission = Permission(
        platform_code=platform_code,
        permission_name=permission_name,
        permission_type=permission_type,
    )
    return ModelManager(permission).save()


def add_role_permissions(role_id, permission_id):
    permission_id = permission_id.split(',')
    role = ModelManager(Role).query_by_id(role_id)
    if not role:
        raise CommonError.NotExist(data={'role_id': role_id})
    model_list = []
    if len(permission_id) > 0:
        permission_map = id_model_map(
            ModelManager(Permission).query_by_ids(permission_id))
        for id in permission_id:
            id = int(id)
            if id in permission_map:
                rp = RolePermission(permission=permission_map[id], role=role)
                model_list.append(rp)
    else:
        permission = ModelManager(Permission).query_by_id(permission_id)
        if not permission:
            raise CommonError.NotExist(data={'permission_id': permission_id})
        rp = RolePermission(permission=permission, role=role)
        model_list.append(rp)
    try:
        db.session.add_all(model_list)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


def query_role_permissions(page_size=15, page_num=1, **kwargs):
    rp_manager = ModelManager(
        RolePermission,
        page_size=page_size,
        page_num=page_num,
        serialize=False
    )
    if kwargs:
        rp_manager.filters = kwargs
    return rp_manager.paginate()



def add_user_role(user_code, role_code):
    role = ModelManager(Role).query_one_by_filter(role_code=role_code)
    if not role:
        raise CommonError.NotExist(data={'role_code': role_code})
    ur = ModelManager(UserRole).query_one_by_filter(
        user_code=user_code,
        role_id=role.id
    )
    if not ur:
        user_role = UserRole(
            user_code=user_code,      
            role=role
        )
        ModelManager(user_role).save()
    return True

def query_user_role(page_size=15, page_num=1, **kwargs):
    ur_manager = ModelManager(
        UserRole,
        page_size=page_size,
        page_num=page_num,
        serialize=False
    )
    if kwargs:
        ur_manager.filters = kwargs
    return ur_manager.paginate()


def remove_user_role(user_code, role_code):
    role = ModelManager(Role).query_one_by_filter(role_code=role_code)
    if not role:
        raise CommonError.NotExist(data={'role_code': role_code})
    qs = (
        db.session
        .query(UserRole).filter(
            UserRole.user_code == user_code,
            UserRole.role_id == role.id
        )
    )
    if qs.one_or_none():
        try:
            qs.delete()
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise e
    return True



def check_permission(user_code, permission_code):
    permission = ModelManager(Permission).query_one_by_filter(
        permission_code=permission_code
    )
    if not permission:
        return False

    role_ids = (
        db.session
        .query(UserRole.role_id)
        .filter(
            UserRole.user_code == user_code, 
            UserRole.status == UserRole.Status.NORMAL.value
        )
    )

    user_role_permissions = (
        db.session
        .query(RolePermission.permission_id)
        .filter(
            RolePermission.permission_id == permission.id,
            RolePermission.role_id.in_(role_ids),
        )
    )
    if user_role_permissions.count() > 0:
        return True
    else:
        return False


def get_platform_permissions(platform_code):
    return ModelManager(Permission).query(platform_code=platform_code)




