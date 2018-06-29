import sys , os , time , requests , json
from flask_restful import Resource, reqparse
from flask import jsonify, request
import datetime
from models import *

class updateCycleSettings(Resource):

	def post(self):
		data = ''
		try:
			data = request.get_json(force = True)
		except :
			print >>sys.stderr, "JSON request not properly formatted"

		print >>sys.stderr, data

		cycleConfig = cycleConfigurationModel()
		cycleConfig.updateCycleSettings(data)

		if cycleConfig.verfifySettings():
			cycleConfig.save()
			return jsonify( {'status' : 'success'} )
		else:
			return jsonify( {'status' : 'error'} )





class getConfiguration(Resource):

	def post(self):
		time = datetime.datetime.now()
		response = {}
		response['hour'] = time.hour
		response['minute'] = time.minute
		response['day'] = time.day
		response['month'] = time.month
		
		configuration = cycleConfigurationModel.getCurrent()

		response.update(configuration.getDict())

		return jsonify(response)

class getConfigurationAndStates(Resource):

	def post(self):
		time = datetime.datetime.now()
		response = {}
		response['hour'] = time.hour
		response['minute'] = time.minute
		response['day'] = time.day
		response['month'] = time.month
		
		configuration = cycleConfigurationModel.getCurrent()
		response.update(configuration.getDict())
		response.update(lightsModel.getStatusDict())

		return jsonify(response)		