from __future__ import division
import sys, os, time, requests, json
from flask_restful import Resource, reqparse
from flask import jsonify, request
from datetime import datetime
from models.models import CycleConfigurationModel, LightsModel, LightModeModel, CycleFeedbackModel, AtmosphereModel
from configuration import Config
import time


class TemperatureHumidity(Resource):

	def post(self):
		# Get Past Feedback for 3 days
		fill_times = AtmosphereModel.get_past_feedback(3)
		temperatures = []
		for log in fill_times:
			point = dict()
			point['x'] = time.mktime(log.created_at.timetuple())
			point['y'] = log.temperature
			temperatures.append(point)

		humidities = []
		for log in fill_times:
			point = dict()
			point['x'] = time.mktime(log.created_at.timetuple())
			point['y'] = log.humidity
			humidities.append(point)

		payload = {
			'temperature': temperatures,
			'humidity': humidities
		}
		return jsonify(payload)


class CycleTimeRatiosChart(Resource):

	def post(self):
		# Get Current Configuration
		current_config = CycleConfigurationModel.get_current()
		air_time = current_config.get_dry_time()
		drain_time = current_config.get_drain_time()
		fill_time = current_config.get_error_time()
		seconds_conversion = 1000
		payload = {
			'air_time': air_time/seconds_conversion,
			'drain_time': drain_time/seconds_conversion,
			'fill_time': fill_time/seconds_conversion
		}
		return jsonify(payload)


class LightTimeRatiosChart(Resource):

	def post(self):
		grow_light = LightsModel.get_light_from_name('growLights')
		schedule = grow_light.get_light_schedule()
		on_time = schedule.stop_time - schedule.start_time
		off_time = 24 - on_time
		payload = {
			'on_time': on_time,
			'off_time': off_time
		}
		return jsonify(payload)


