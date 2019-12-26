__NAMESPACE__ = 'storage'

MONGODB_HOST = 'mongodb.dev'
MONGODB_PORT = 27017
MONGODB_DB = 'distributor'

SQLALCHEMY_ENGINE_OPTIONS = {
    'isolation_level': 'READ_COMMITTED',
    'pool_pre_ping': True,  # 2006, "MySQL server has gone away"
}

CACHE_REDIS = {
    'host': 'cacheredis.dev',
    'port': 23579,
    'db': 8,
}

PERSIST_REDIS = {
    'host': 'persistredis.dev',
    'port': 23580,
    'db': 8,
}

ZOOKEEPER = {
    'hosts': 'zookeeper.dev:2181',
    'timeout': 10,
    'auth_data': None,
}

CACHE_CONFIG = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 5,
    'CACHE_THRESHOLD': 1000,
}

API_SECRET = ''
SQLALCHEMY_DATABASE_URI = ''
