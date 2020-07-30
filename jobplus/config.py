class BaseConfig(object):
    SECRET_KEY = 'very secret key'
    INDEX_PER_PAGE = 9
    ADMIN_PER_PAGE = 15
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8'
#    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://devops:devops38@demo02:3309/jobplus?charset=utf8'

class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
