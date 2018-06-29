import sys , os , time , requests , json
from flask_restful import Resource, reqparse
from flask import jsonify, request
import datetime

class change(Resource):
	
	def post(self):
		data = ''
		try:
			data = request.get_json(force = True)
		except :
			print >>sys.stderr, "JSON request not properly formatted"

		print >>sys.stderr, data['state']
		payload = {'command':'manualLightSwitch','light': data['light'],'state':data['state']}
		headers = {'Content-Type': 'application/json'}
		r = requests.post('http://192.168.0.2', data = json.dumps(payload))
		return