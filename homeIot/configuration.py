
class Config(object):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/QuickHire'	
	SECRET_KEY='secret!'
	SQLALCHEMY_TRACK_MODIFICATIONS= 'FALSE'
	TESTING = 

class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
	pass	

class TestingConfig(Config):
	pass


