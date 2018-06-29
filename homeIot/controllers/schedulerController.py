import sys , os , time , requests , json
from flask_restful import Resource, reqparse
from flask import jsonify, request
import datetime




class giveServerTime(Resource):
    
	
	def get(self):
		
		time = datetime.datetime.now()
		response = {}
		response['hour'] = time.hour
		response['minute'] = time.minute
		response['day'] = time.day
		response['month'] = time.month
		
		return jsonify(response)

class changeLightSchedule(Resource):

	def get(self):
		
		payload = {'command':'manualLightSwitch','light': 'tankLights','state':'on'}
		data = jsonify(payload)
		headers = {'Content-Type': 'application/json'}
		r = requests.post('http://192.168.0.2', data = json.dumps(payload))
		return