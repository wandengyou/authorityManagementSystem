import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

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
    users, total = user_manager.paginate()
    if total > 0:
        user_role_map = user_role_statistic()
        for user in users:
            user['role_total'] = user_role_map.get(
                user['user_code'], 0
            )
    return users, total


def query_platform(page_size=15, page_num=1, **kwargs):
    platform_manager = ModelManager(
        Platform,
        page_size=page_size,
        page_num=page_num
    )
    if kwargs:
        platform_manager.filters = kwargs
    
    platforms, total = platform_manager.paginate()

    if total > 0:
        permission_map = platform_permission_statistic()
        role_map = platform_role_statistic()
        user_map = platform_user_statistic()
        for platform in platforms:
            platform['permission_total'] = permission_map.get(
                platform['platform_code'], 0
            )
            platform['role_total'] = role_map.get(
                platform['platform_code'], 0
            )
            platform['user_total'] = user_map.get(
                platform['platform_code'], 0
            )
    return platforms, total


def add_platform(platform_name, **kwargs):
    platform = Platform(
        platform_name=platform_name,
    )
    if kwargs:
        for key, value in kwargs.items():
            setattr(platform, key, value)
    return ModelManager(platform).save()


def platform_handle(platform_code, status, **kwargs):
    platform_manager = ModelManager(Platform)
    platform = platform_manager.query_one_by_filter(platform_code=platform_code)
    if not platform:
        raise CommonError.NotExist(data={'platform_code': platform_code})
    platform_manager.update(status=status, **kwargs)
    return True



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
    roles, total = role_manager.paginate()
    if total > 0:
        permission_map = role_permission_statistic()
        for role in roles:
            role['permission_total'] = permission_map.get(
                role['id'], 0
            )
    return roles, total


def update_role(role_code, **kwargs):
    role_manager = ModelManager(Role)
    role = role_manager.query_one_by_filter(role_code=role_code)
    if not role:
        raise CommonError.NotExist(data={'role_code': role_code})
    role_manager.update(**kwargs)
    return True


def query_permission(page_num=1, page_size=15, **kwargs):
    permission_manager = ModelManager(
        Permission, 
        page_size=page_size, 
        page_num=page_num
    )
    if kwargs:
        permission_manager.filters = kwargs
    return permission_manager.paginate()


def add_permission(platform_code, permission_name, permission_type, identifier):
    permission = Permission(
        platform_code=platform_code,
        permission_name=permission_name,
        permission_type=permission_type,
        identifier=identifier
    )
    return ModelManager(permission).save()


def update_permission(permission_code, **kwargs):
    permission_manager = ModelManager(Permission)
    permission = permission_manager.query_one_by_filter(
        permission_code=permission_code
    )
    if not permission:
        raise CommonError.NotExist(data={'permission_code': permission_code})
    permission_manager.update(**kwargs)
    return True


def add_role_permissions(role_code, permission_code):
    permission_code_list = permission_code.split(',')
    role = ModelManager(Role).query_one_by_filter(role_code=role_code)
    if not role:
        raise CommonError.NotExist(data={'role_code': role_code})
    
    db_role_permissions = ModelManager(RolePermission).query(role_id=role.id)
    model_list, surplus_permission = [], []
    if db_role_permissions:
        db_code_list = [
            rp.permission.permission_code 
            for rp in db_role_permissions
        ]
        surplus_permission = list(
            set(permission_code_list) -set(db_code_list)
        )
    else:
        surplus_permission = permission_code_list
    if len(surplus_permission) > 0:
        qs = (
            db.session
            .query(Permission)
            .filter(Permission.permission_code.in_(surplus_permission))
        )
        if qs.count() > 0:
            permission_map = id_model_map(qs.all(), 'permission_code')
            for code in permission_code_list:
                if code in permission_map:
                    rp = RolePermission(permission=permission_map[code], role=role)
                    model_list.append(rp)
        else:
            raise CommonError.NotExist(data={
                'permission_code_list': surplus_permission
            })
    try:
        db.session.add_all(model_list)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise
    return True


def remove_role_permissions(role_code, permission_code):
    permission_code_list = permission_code.split(',')
    role = ModelManager(Role).query_one_by_filter(role_code=role_code)
    if not role:
        raise CommonError.NotExist(data={'role_code': role_code})
    qs = db.session
    permission_ids = (
        qs
        .query(Permission.id)
        .filter(Permission.permission_code.in_(permission_code_list))
    )
    qs = (
        qs
        .query(RolePermission)
        .filter(
            RolePermission.role_id == role.id, 
            RolePermission.permission_id.in_(permission_ids)
        )
    )
    if qs.count() > 0:
        try:
            qs.delete(synchronize_session=False)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
    return True


def query_role_permissions(page_size=15, page_num=1, **kwargs):
    rp_manager = ModelManager(
        RolePermission,
        page_size=page_size,
        page_num=page_num,
        serialize=False
    )
    if kwargs:
        role = ModelManager(Role).query_one_by_filter(
            role_code=kwargs['role_code']
        )
        if not role:
            raise CommonError.NotExist(data={'role_code': kwargs['role_code']})
        rp_manager.filters = {'role_id': role.id}
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
        except SQLAlchemyError:
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


def get_user_permissions(user_code):
    qs = db.session
    role_ids = (
        qs.query(UserRole.role_id)
        .filter(
            UserRole.user_code == user_code,
            UserRole.status == UserRole.Status.NORMAL.value
        )
    )
    role_permissions = (
        qs.query(RolePermission)
        .filter(RolePermission.role_id.in_(role_ids))
    )
    permissions = []
    total = role_permissions.count()
    if total > 0:
        permissions = [rp.permission for rp in role_permissions]
    return permissions, total


def get_user_role(user_code, page_size=15, page_num=1):
    user = ModelManager(User).query_one_by_filter(user_code=user_code)
    if not user:
        raise CommonError.NotExist(data={'user_code': user_code})
    manager = ModelManager(
        UserRole,
        page_size=page_size,
        page_num=page_num,
        serialize=False,
        filters={'user_code':user_code}
    )
    user_roles, total = manager.paginate()
    roles = []
    if total > 0:
        role_permission_map = role_permission_statistic()
        for ur in user_roles:
            role = ur.role.to_dict()
            role['permission_total'] = role_permission_map.get(
                role['id'], 0
            )
            roles.append(role)
    return roles, total

def import_permission(platform_code, data_stream, **kwargs):
    df = pd.read_json(data_stream)
    permissions = []
    for index, row in df.iterrows():
        permission = Permission(
            platform_code=platform_code,
            permission_name=row.permission_name,
            permission_type=row.permission_type,
            identifier=row.identifier
        )
        permissions.append(permission)
    if 'storage' in kwargs and kwargs['storage'] > 0:
        try:
            db.session.add_all(permissions)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
    return permissions




def platform_permission_statistic(platform_code=None):
    qs = (
        db.session.query(Permission.platform_code,
                         func.count(Permission.id).label('count'))
        .group_by(Permission.platform_code)
    )
    if platform_code:
        qs.filter_by(platform_code == platform_code)
    permission_map = {}
    if qs.count() > 0:
        for statistic in qs.all():
            permission_map[statistic.platform_code] = statistic.count
    return permission_map


def platform_role_statistic(platform_code=None):
    qs = (
        db.session.query(Role.platform_code,
                         func.count(Role.id).label('count'))
        .group_by(Role.platform_code)
    )
    if platform_code:
        qs.filter_by(platform_code == platform_code)
    role_map = {}
    if qs.count() > 0:
        for statistic in qs.all():
            role_map[statistic.platform_code] = statistic.count
    return role_map


def platform_user_statistic(platform_code=None):
    qs = (
        db.session.query(User.platform_code,
                         func.count(User.id).label('count'))
        .group_by(User.platform_code)
    )
    if platform_code:
        qs.filter_by(platform_code == platform_code)
    user_map = {}
    if qs.count() > 0:
        for statistic in qs.all():
            user_map[statistic.platform_code] = statistic.count
    return user_map


def role_permission_statistic(role_id=None):
    qs = (
        db.session.query(
            RolePermission.role_id,
            func.count(RolePermission.id).label('count')
        )
        .group_by(RolePermission.role_id)
    )
    print(qs)
    if role_id:
        qs.filter_by(role_id == role_id)
    role_permission_map = {}
    if qs.count() > 0:
        for statistic in qs.all():
            role_permission_map[statistic.role_id] = statistic.count
    return role_permission_map


def user_role_statistic(user_code=None):
    qs = (
        db.session.query(
            UserRole.user_code,
            func.count(UserRole.id).label('count')
        )
        .group_by(UserRole.user_code)
    )
    if user_code:
        qs.filter_by(user_code == user_code)
    user_role_map = {}
    if qs.count() > 0:
        for statistic in qs.all():
            user_role_map[statistic.user_code] = statistic.count
    return user_role_map



