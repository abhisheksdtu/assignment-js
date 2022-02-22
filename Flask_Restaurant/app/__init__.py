from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from apispec import APISpec
from flask_restful import Resource, Api
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

application = Flask(__name__)
application.secret_key = 'flask-restraunt-1234'

# RESTFUL FLASK WRAPS FLASK APP AROUND IT
api = Api(application)  

application.config.update({
    'APISPEC_SPEC': APISpec(
        title='Zomato System Design',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    # URI FOR ACCESSING API DOC IN JSON
    'APISPEC_SWAGGER_URL': '/swagger/',  
    # URI FOR ACCESSING UI OF API DOC
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  
})
docs = FlaskApiSpec(application)

from app.models import *