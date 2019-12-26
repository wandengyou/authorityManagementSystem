import string
from enum import Enum
from random import sample
from time import time

from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship

letters = string.ascii_letters + string.digits


def random_short_string(size=6):
    return ''.join(sample(letters, size))


@as_declarative(name='BaseModel')
class BaseModel:
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_time = Column(
        BigInteger, index=True, default=lambda: int(time()) * 1000,
    )
    updated_time = Column(BigInteger, default=0)

    __abstract__ = True

    # __bind_key__ = 'default'

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__mapper__.c}


class Platform(BaseModel):
    class Status(Enum):
        DELETE = -1  # 删除
        FORBIDDEN = 0
        USED = 1

    platform_name = Column(String(40), nullable=False)
    platform_code = Column(String(40), unique=True, index=True, nullable=False)
    platform_host = Column(String(120), nullable=False)
    status = Column(Integer, server_default=str(Status.USED.value))
    description = Column(String(200))

    __tablename__ = 'platform'


class Role(BaseModel):
    platform_code = Column(String(40), nullable=False)
    role_name = Column(String(40), nullable=False)
    role_code = Column(String(40), unique=True, index=True, nullable=False)
    description = Column(String(200))

    __tablename__ = 'role'


class UserRole(BaseModel):
    class Status(Enum):
        DELETE = -1  # 删除
        FORBIDDEN = 0
        NORMAL = 1

    user_code = Column(String(40), nullable=False)
    platform_code = Column(String(40), nullable=False)
    role_id = Column(BigInteger, nullable=False)
    role = relationship(
        'Role',
        foreign_keys=role_id,
        primaryjoin='Role.id == UserRole.role_id',
        uselist=False,
        backref='user_role_role'
    )
    status = Column(Integer, server_default=str(Status.NORMAL.value))

    __tablename__ = 'user_role'


class Menu(BaseModel):
    platform_code = Column(String(40), nullable=False)
    parent_id = Column(BigInteger, server_default='0')
    menu_name = Column(String(40), nullable=False)
    menu_code = Column(String(40), unique=True, index=True, nullable=False)
    menu_level = Column(Integer, nullable=False)
    sequence = Column(Integer, server_default='1')  # 菜单顺序

    __tablename__ = 'menu'


class MenuHandle(BaseModel):
    platform_code = Column(String(40), nullable=False)
    menu_id = Column(BigInteger, nullable=False)
    handle_name = Column(String(40), nullable=False)
    handle_code = Column(String(40), unique=True, index=True)
    api_path = Column(String(128))
    api_host = Column(String(128))
    api_params = Column(String(400))
    api_md5 = Column(String(200))  # md5(api_path + api_host)
    api_remarks = Column(String(200))
    catalog = Column(String(40), nullable=False)  # menu order  : 1/3/11

    __tablename__ = 'menu_handle'


class RoleHandle(BaseModel):
    handle_id = Column(BigInteger, nullable=False)
    handle = relationship(
        'MenuHandle',
        foreign_keys=handle_id,
        primaryjoin='MenuHandle.id == RoleHandle.handle_id',
        uselist=False,
        backref='role_handle_handel'
    )
    role_id = Column(BigInteger, nullable=False)
    role = relationship(
        'Role',
        foreign_keys=role_id,
        primaryjoin='Role.id == RoleHandle.role_id',
        uselist=False,
        backref='role_handle_role'
    )

    __tablename__ = 'role_handle'
