import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
sys.dont_write_bytecode = True
from flask_cors import CORS

app = Flask(__name__) 
app.config.from_object(__name__)
app.config.update(
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/aquaponics',
	SECRET_KEY='secret!',
	JWT_SECRET_KEY= 'jwt-secret-string',
	SQLALCHEMY_TRACK_MODIFICATIONS= 'false',
	TEMPLATES_AUTO_RELOAD = True,
	)

#app.config.from_object('configuration.DevelopmentConfig')

mobileAPI = Api(app)

#Create DB ORM instance
db = SQLAlchemy(app)

migrate = Migrate(app , db)

CORS(app)

#Import Controllers now that DB is instanciated
import controllers.schedulerController as schedulerController, controllers.dataCollectionController as dataCollectionController, controllers.lightController as lightController , controllers.cycleSettingsController as cycleSettingsController
from models import *

#LandingPage for WebApp
@app.route('/')
def landingController():
	return render_template('landingPage.html')



mobileAPI.add_resource(schedulerController.giveServerTime, '/API/getTime')
mobileAPI.add_resource(schedulerController.changeLightSchedule, '/API/test')
mobileAPI.add_resource(dataCollectionController.collect, '/API/data')
mobileAPI.add_resource(lightController.change,'/API/changeLightSchedule')
mobileAPI.add_resource(cycleSettingsController.updateCycleSettings,'/API/updateCycleSettings')
mobileAPI.add_resource(cycleSettingsController.getConfiguration, '/API/getConfiguration')
mobileAPI.add_resource(cycleSettingsController.getConfigurationAndStates, '/API/loadSettings')

#run on global
app.run(host='0.0.0.0')