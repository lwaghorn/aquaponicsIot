from flask_sqlalchemy import SQLAlchemy
from homeIot import db
import datetime
import sys

class lightScheduleModel(db.Model):

	__tablename__ ='lightSchedules'

	id = db.Column(db.Integer, primary_key=True)
	light_id = db.Column(db.String(120), unique = True, nullable = False)
	start_time = db.Column(db.Integer, nullable=False)
	stop_time = db.Column(db.Integer, nullable=False)

	@staticmethod
	def getFromLightId(givenId):
		obj = lightScheduleModel()
		return obj.query.filter_by(light_id = givenId).first()

	def getStartTime(self):
		return self.start_time

	def getStopTime(self):
		return self.stop_time

	def save(self):
		db.session.add(self)
		db.session.commit()



class manualLightSwithcesModel(db.Model):
	
	__tablename__ ='manualLightSwitch'	

	id = db.Column(db.Integer, primary_key=True)
	light_id = db.Column(db.Integer, unique = True, nullable = False)
	mode = db.Column(db.Integer, nullable=False)

	def save(self):
		db.session.add(self)
		db.session.commit()


class lightsModel(db.Model):
	
	__tablename__='lights'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique = True, nullable = False)

	@staticmethod
	def getAll():
		obj = lightsModel()
		return obj.query.all()


	def getStatus(self):
		lightSchedule = lightScheduleModel.getFromLightId(self.id)
		time = datetime.datetime.now()
		if lightSchedule.getStartTime > time.hour and lightSchedule.getStopTime < time.hour:
			return 1
		else:
			return 0

	def getMode(self):
		return 1


	@staticmethod
	def getStatusDict():
		lights = lightsModel.getAll()
		response = []
		for light in lights:
			lightDict = {}
			lightDict['lightName'] = light.name
			lightDict['status'] = light.getStatus()
			lightDict['mode'] = light.getMode()
			response.append(lightDict)
		print >>sys.stderr, response
		return response

class atmosphereModel(db.Model):

	__tablename__ = 'atmosphere'

	id = db.Column(db.Integer, primary_key=True)
	temperature = db.Column(db.Float, nullable=False)
	humidity = db.Column(db.Float, nullable=False)
	light = db.Column(db.Float, nullable=False)

	def save(self):
		db.session.add(self)
		db.session.commit()


class cycleConfigurationModel(db.Model):

	__tablename__ = 'cycleConfiguration'

	id = db.Column(db.Integer, primary_key=True)
	threshold = db.Column(db.Integer, nullable=False)
	dry_time = db.Column(db.Integer, nullable=False)
	error_time = db.Column(db.Integer, nullable=False)
	drain_time = db.Column(db.Integer , nullable=False)
	dc_pulse = db.Column(db.Integer , nullable=False)

	def save(self):
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def getCurrent():
		obj = cycleConfigurationModel()
		return obj.query.order_by('-id').first()

	def updateCycleSettings(self,data):
		self.threshold = data['threshold']
		self.dry_time = data['dryTime']
		self.error_time = data['errorTime']
		self.drain_time = data['drainTime']
		self.dc_pulse = data['dcPulse']
		return

	def verfifySettings(self):
		return True

	def getDict(self):
		response = {}
		response['threshold'] = self.threshold
		response['drainTime'] = self.drain_time
		response['errorTime'] = self.error_time
		response['dryTime'] = self.dry_time
		response['dcPulse'] = self.dc_pulse
		return response;
