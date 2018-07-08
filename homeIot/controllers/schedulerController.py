import sys, os, time, requests, json
from flask_restful import Resource, reqparse
from flask import jsonify, request
import datetime


class GiveServerTime(Resource):

    def get(self):
        current_time = datetime.datetime.now()
        response = dict()
        response['hour'] = current_time.hour
        response['minute'] = current_time.minute
        response['day'] = current_time.day
        response['month'] = current_time.month
        return jsonify(response)


class ChangeLightSchedule(Resource):

    def get(self):
        payload = {'command': 'manualLightSwitch','light': 'tankLights','state':'on'}
        data = jsonify(payload)
        headers = {'Content-Type': 'application/json'}
        r = requests.post('http://192.168.0.2', data=json.dumps(payload))
        return

