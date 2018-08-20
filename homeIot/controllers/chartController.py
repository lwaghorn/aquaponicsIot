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