from __future__ import division
import sys, os, time, requests, json
from flask_restful import Resource, reqparse
from flask import jsonify, request
from datetime import datetime
from models.models import CycleConfigurationModel, LightsModel, LightModeModel, CycleFeedbackModel, AtmosphereModel
from configuration import Config
import time
from pytz import timezone


class UpdateCycleSettings(Resource):

	def post(self):
		data = request.get_json(force=True)
		print >> sys.stderr, data
		if data['password'] == Config.UPDATE_PASSWORD:
			print >> sys.stderr, 'passwordpass'
			cycle_config = CycleConfigurationModel()
			cycle_config.set_cycle_settings(data)
			if cycle_config.verfify_settings():
				cycle_config.save()
				payload = cycle_config.get_dict()
				payload['command'] = 'cycleSettings'
				requests.post(Config.ARDUINO_IP, data=json.dumps(payload))
				return jsonify({'status': 'success'})
			else:
				return jsonify({'status': 'fail', 'error': 'Incorrect Password'})
		else:
			print >> sys.stderr, 'password FAIL'
			return jsonify({'status': 'fail', 'error': 'Incorrect Password'})


class GetConfiguration(Resource):

	def get(self):
		current_time = datetime.now()
		response = dict()
		response['hour'] = current_time.hour
		response['minute'] = current_time.minute
		configuration = CycleConfigurationModel.get_current()
		response.update(configuration.get_dict())
		LightModeModel.reset_modes()
		return jsonify(response)


class GetConfigurationArduino(Resource):

	def get(self):
		utc = datetime.now(timezone('UTC'))
		local_time = utc.astimezone(timezone('Canada/Newfoundland'))
		response = dict()
		response['hour'] = local_time.hour
		response['minute'] = local_time.minute
		configuration = CycleConfigurationModel.get_current()
		response.update(configuration.get_dict())
		response.pop('dcPulse', None)
		LightModeModel.reset_modes()
		return jsonify(response)


class GetConfigurationAndStates(Resource):

	def post(self):
		current_time = datetime.now()
		response = dict()
		response['hour'] = current_time.hour
		response['minute'] = current_time.minute
		response['day'] = current_time.day
		response['month'] = current_time.month
		configuration = CycleConfigurationModel.get_current()
		response['configuration'] = configuration.get_dict()
		response['lightStatuses'] = LightsModel.get_status_dict()
		return jsonify(response)


class Change(Resource):

	def post(self):
		data = ''
		try:
			data = request.get_json(force=True)
		except:
			print >> sys.stderr, "JSON request not properly formatted"
		light = data['light']
		state = data['state']
		payload = {'command': 'manualLightSwitch', 'light': light, 'state': state}
		requests.post(Config.ARDUINO_IP, data=json.dumps(payload))
		LightModeModel.log_change(light=light, state=state)
		return


