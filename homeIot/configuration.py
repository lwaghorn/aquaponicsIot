
class Config(object):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/QuickHire'	
	SECRET_KEY='secret!'
	SQLALCHEMY_TRACK_MODIFICATIONS = 'FALSE'
	ARDUINO_IP = 'http://99.253.59.150'
	UPDATE_PASSWORD = 'fishy'


class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
	pass	

class TestingConfig(Config):
	pass


