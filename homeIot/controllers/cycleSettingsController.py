import sys, os, time, requests , json
from flask_restful import Resource, reqparse
from flask import jsonify, request
import datetime
from models.models import CycleConfigurationModel, LightsModel, LightModeModel
from configuration import Config


class UpdateCycleSettings(Resource):

    def post(self):
        data = request.get_json(force=True)
        print >>sys.stderr, data
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
                return jsonify({'status': 'error'})
        else:
            print >> sys.stderr, 'password FAIL'
            return jsonify({'status': 'error'})


class GetConfiguration(Resource):

    def get(self):
        current_time = datetime.datetime.now()
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
        current_time = datetime.datetime.now()
        response = dict()
        response['hour'] = current_time.hour
        response['minute'] = current_time.minute
        response['day'] = current_time.day
        response['month'] = current_time.month
        configuration = CycleConfigurationModel.get_current()
        response['configuration']=configuration.get_dict()
        response['lightStatuses']=LightsModel.get_status_dict()
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

