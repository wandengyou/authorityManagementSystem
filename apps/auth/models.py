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
    platform_code = Column(String(40), unique=True, index=True, default=random_short_string)
    platform_host = Column(String(120), nullable=False)
    status = Column(Integer, server_default=str(Status.USED.value))
    description = Column(String(200))

    __tablename__ = 'platform'


class Role(BaseModel):

    platform_code = Column(String(40), nullable=False)
    role_name = Column(String(40), nullable=False)
    role_code = Column(String(40), unique=True, index=True,
                       default=random_short_string
                      )
    description = Column(String(200))

    __tablename__ = 'role'


class User(BaseModel):

    user_code = Column(String(40), nullable=False)
    platform_code = Column(String(40), nullable=False)

    __tablename__ = 'user'


class UserRole(BaseModel):

    class Status(Enum):
        DELETE = -1  # 删除
        FORBIDDEN = 0
        NORMAL = 1

    user_code = Column(String(40), nullable=False)
    role_id = Column(BigInteger)
    role = relationship(
        'Role',
        foreign_keys=role_id,
        primaryjoin='Role.id == UserRole.role_id',
        uselist=False,
        backref='user_role'
    )
    status = Column(Integer, server_default=str(Status.NORMAL.value))

    __tablename__ = 'user_role'


class Permission(BaseModel): 
    
    class Status(Enum):
        DELETE = -1  # 删除
        FORBIDDEN = 0
        NORMAL = 1

    platform_code = Column(String(40), nullable=False)
    permission_name = Column(String(40), nullable=False)
    permission_code = Column(String(40), unique=True, index=True,
                             default=random_short_string
                            )
    permission_type = Column(Integer, nullable=False)
    status = Column(Integer, server_default=str(Status.NORMAL.value))

    __tablename__ = 'permission'


class RolePermission(BaseModel):

    permission_id = Column(BigInteger, nullable=False)
    permission = relationship(
        'Permission',
        foreign_keys=permission_id,
        primaryjoin='Permission.id == RolePermission.permission_id',
        uselist=False,
        backref='permission'
    )
    role_id = Column(BigInteger, nullable=False)
    role = relationship(
        'Role',
        foreign_keys=role_id,
        primaryjoin='Role.id == RolePermission.role_id',
        uselist=False,
        backref='role'
    )

    __tablename__ = 'role_permission'

