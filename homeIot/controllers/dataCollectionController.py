import sys , os , time , requests , json
from flask_restful import Resource, reqparse
from flask import jsonify, request
from models.models import AtmosphereModel, CycleFeedbackModel



class Collect(Resource):

    def post(self):
        try:
            data = request.get_json(force=True)
        except:
            print >>sys.stderr, "JSON request not properly formatted"
        print >>sys.stderr, data
        atmosphere = AtmosphereModel(temperature=data['temperature'], humidity=data['humidity'], light=data['light'])
        atmosphere.save()

        feed_back = CycleFeedbackModel()
        feed_back.log_cylce_feedback()
        return


