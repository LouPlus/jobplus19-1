import os


class Base:
    '''配置类基类
    '''

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asdfasdf'
    SQLALCHEMY_TRACK_MODIFICATION = False


class DevelopConfig(Base):
    '''开发环境配置类
    '''

    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/jobplus?charset=utf8'


class ProduceConfig(Base):
    '''生产环境配置类
    '''

    pass


configs = {
        'dev': DevelopConfig,
        'pro': ProduceConfig
}
