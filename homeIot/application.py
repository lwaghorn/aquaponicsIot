import os
from flask import Flask, render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
from flask_cors import CORS

#sys.path.append('/home/liam/Developement/Flask/AquaponicsIot/aquaponicsIot/homeIot/')
from controllers import cycleSettingsController, dataCollectionController, schedulerController

sys.dont_write_bytecode = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
                  SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@localhost/aquaponics',
                  SECRET_KEY='secret!',
                  JWT_SECRET_KEY='jwt-secret-string',
                  SQLALCHEMY_TRACK_MODIFICATIONS='false',
                  TEMPLATES_AUTO_RELOAD=True
                    )
mobileAPI = Api(app)
CORS(app)
#app.config.from_object('configuration.DevelopmentConfig')



@app.route('/')
def landing_controller():
    return render_template('landingPage.html')


mobileAPI.add_resource(schedulerController.GiveServerTime, '/API/getTime')
mobileAPI.add_resource(schedulerController.ChangeLightSchedule, '/API/test')
mobileAPI.add_resource(dataCollectionController.Collect, '/API/data')
mobileAPI.add_resource(cycleSettingsController.Change, '/API/toggleLight')
mobileAPI.add_resource(cycleSettingsController.UpdateCycleSettings, '/API/updateCycleSettings')
mobileAPI.add_resource(cycleSettingsController.GetConfiguration, '/API/getConfiguration')
mobileAPI.add_resource(cycleSettingsController.GetConfigurationAndStates, '/API/loadSettings')

from models.models import db
db.init_app(app)
migrate = Migrate(app, db)

app.run(host='0.0.0.0', port=5001)
