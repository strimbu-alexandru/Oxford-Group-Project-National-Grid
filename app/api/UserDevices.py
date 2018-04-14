from flask import Flask, url_for, request, render_template, Blueprint, json, Response, session
from flask_restful import Resource, Api

from app.Models import UserDevices, User
from app.api.AuthMethods import authMethods
from app.Database import db_session
from app.ErrorHandler import CustomError
from config import Config

UserDevices = Blueprint('UserDevices',__name__, url_prefix='/userDevices', template_folder='templates')
api = Api(UserDevices)

def getUserId(authToken):
		user = authMethods.findUserByToken			#get the userId from User database
		return user.userId

class AddUserDevices(Resource):						#add a new user device using the token to identify the user
	def post(self):
		authToken = request.form['authToken']		#get the parameters from the form
		userId = getUserId(authToken)
		deviceName = request.form['deviceName']
		consumption = request.form['consumption']
		timeToCharge = request.form['timeToCHarge']
		userDevices = UserDevices(userId = userId, deviceName = deviceName, consumption = consumption, timeToCHarge = timeToCharge)		#if user is valid, proceed to enter it into the user database
		db_session.add(userDevices)
		db_session.commit()
		return "User added successfully!"
		
class GetUserDevices(Resource):
	def get(self):
		authToken = request.form['authToken']		#get the parameters from the form
		userId = getUserId(authToken)
		userDevices = UserDevices.query.filter(UserDevices.userId == userID)
		return json.dumps(userDevices)
		
class DeleteUserDevice(Resource):					#deletes an entry based on userId and deviceName
	def get(self):
		authToken = request.form['authToken']		#get the parameters from the form
		userId = getUserId(authToken)
		deviceName = request.form['deviceName']
		userDevice = UserDevices.query.filter(UserDevices.userId == userID, UserDevices.deviceName == deviceName).first()
		if userDevice != None :						#check if the user device exists
			db_session.delete(userDevice)			#then delete it
			db_session.commit()
			return "Device deleted successfully!"
		return "Device not found in the database!"
		
class DeleteAllUserDevices(Resource):				#deletes all the devices for a user
	def get(self):
		authToken = request.form['authToken']		#get the parameters from the form
		userId = getUserId(authToken)
		userDevices = UserDevices.query.filter(UserDevices.userId == userID)    #get all the devices
		for item in userDevices :
			db_session.delete(item)
		db_session.commit()
		return "Devices deleted successfully"
	

api.add_resource(AddUserDevices, '/add')
api.add_resource(GetUserDevices, '/get')
api.add_resource(DeleteUserDevice, '/delete')
api.add_resource(DeleteAllUserDevices, '/deleteAll')

