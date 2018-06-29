import sys , os , time , requests , json
from flask_restful import Resource, reqparse
from flask import jsonify, request
import datetime




class collect(Resource):
    
	
	def post(self):	
		try:
			data = request.get_json(force = True)
		except :
			print >>sys.stderr, "JSON request not properly formatted"

		print >>sys.stderr, data
		
		return

		atmo = atmosphereModel(temperature = data['temperature'] , humidity= data['humidity'] , light = data['light'] )
		atmo.save()

		#When the tank is not cycling it doesnt send cycle settings
  		if 'threshold' in data.keys():
			cycleConfig = cycleConfigurationModel(threshold =  data['threshold'] , fillTime = data['waterInRunTime'] , drainTime =  data['drainTime'] , errorTime = data['errorTime'] )
			cycleConfig.save()
		
		return

			
			