from . import storage

storage.SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'.format(
    user='root',
    password='123456',
    host='192.168.0.14',
    port=3306,
    database='auth'
)

AccessKey = 'access'
SecretKey = 'secret'
