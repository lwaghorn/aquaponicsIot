from __future__ import division
import sys, os, time, requests, json
from flask_restful import Resource, reqparse
from flask import jsonify, request
from datetime import datetime
from models.models import CycleConfigurationModel, LightsModel, LightModeModel, CycleFeedbackModel
from configuration import Config
import time


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
		response['day'] = current_time.day
		response['month'] = current_time.month
		configuration = CycleConfigurationModel.get_current()
		response.update(configuration.get_dict())
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


class WaterInTimeChart(Resource):

	def post(self):
		# Get Past Feedback for 3 days
		fill_times = CycleFeedbackModel.get_past_feedback(3)
		fill_time_coordinates = []
		for log in fill_times:
			point = dict()
			point['x'] = time.mktime(log.created_at.timetuple())
			point['y'] = log.time_to_fill/1000
			fill_time_coordinates.append(point)

		configuration = CycleConfigurationModel.get_current()
		max_fill_time = configuration.get_error_time()/1000
		max_fill_time_coordinates = []
		max_fill_point_start = dict(x=time.mktime(fill_times[0].created_at.timetuple()), y=max_fill_time)
		max_fill_point_end = dict(x=time.mktime(fill_times[-1].created_at.timetuple()), y=max_fill_time)
		max_fill_time_coordinates.extend([max_fill_point_start, max_fill_point_end])
		payload = {
			'fill_time_data': fill_time_coordinates,
			'maximum_fill_time_data': max_fill_time_coordinates
		}
		return jsonify(payload)


class CycleTimeRatiosChart(Resource):

	def post(self):
		# Get Current Configuration
		current_config = CycleConfigurationModel.get_current()
		air_time = current_config.get_dry_time()
		drain_time = current_config.get_drain_time()
		last_cycle = CycleFeedbackModel.get_last_cycle()
		last_fill_time = last_cycle.get_time_to_fill()
		seconds_conversion = 1000
		payload = {
			'air_time': air_time/seconds_conversion,
			'drain_time': drain_time/seconds_conversion,
			'fill_time': last_fill_time/seconds_conversion
		}
		return jsonify(payload)

