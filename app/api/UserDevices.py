from flask import Flask, url_for, request, render_template, Blueprint, json, Response, session
from flask_restful import Resource, Api

from app.Models import UserDevice, User
from app.api.AuthMethods import authMethods
from app.api.ChargingSlots import ChargingSlotMethods
from app.Database import db_session
from app.ErrorHandler import CustomError
from config import Config
from app.api.Auth import login_required

UserDevices = Blueprint('UserDevices',__name__, url_prefix='/userDevices', template_folder='templates')
api = Api(UserDevices)

def getUserId():
	#get the userId from User database
	authToken = authMethods.getAuthTokenFromJWT(session['JWT'])
	user = authMethods.findUserByToken(authToken)
	return user.userId

class AddUserDevices(Resource):						#add a new user device using the token to identify the user
	@login_required
	def post(self):
		userId = getUserId()
		#get the parameters from the form
		deviceName = request.form['deviceName']
		consumption = request.form['consumption']
		timeToCharge = request.form['timeToCharge']
		userDevice = UserDevice.query.filter(UserDevice.userId == userId, UserDevice.deviceName == deviceName).first()
		if userDevice != None :
			return "used"
		userDevices = UserDevice(userId = userId, deviceName = deviceName, consumption = consumption, timeToCharge = timeToCharge)
		db_session.add(userDevices)
		db_session.commit()
		return "success"

class GetUserDevices(Resource):
	@login_required
	def get(self):
		userId = getUserId()
		userDevices = UserDevice.query.filter(UserDevice.userId == userId).all()

		# Serialise the user devices returned.
		def dictify(UserDevice):
			return UserDevice._asdict()
		UserDevicesDict = list(map(dictify, userDevices))

		return UserDevicesDict

class DeleteUserDevice(Resource):					#deletes an entry based on userId and deviceName
	@login_required
	def get(self, deviceName):
		userId = getUserId()
		userDevice = UserDevice.query.filter(UserDevice.userId == userId, UserDevice.deviceName == deviceName).first()
		if userDevice != None :													#check if the user device exists
			ChargingSlotMethods.removeSlotByDevice(userDevice.deviceId, userId)	#delete any associated charging slots
			db_session.delete(userDevice)										#then delete device
			db_session.commit()
			return "Device deleted successfully!"
		return "Device not found in the database!"

class DeleteAllUserDevices(Resource):				#deletes all the devices for a user
	@login_required
	def get(self):
		userId = getUserId()
		userDevices = UserDevice.query.filter(UserDevice.userId == userId).all()    #get all the devices
		for item in userDevices :
			# Delete associated charging slots
			ChargingSlotMethods.removeSlotByDevice(item.deviceId, userId)
			db_session.delete(item)
		db_session.commit()
		return "Devices deleted successfully"


api.add_resource(AddUserDevices, '/add')
api.add_resource(GetUserDevices, '/get')
api.add_resource(DeleteUserDevice, '/delete/<deviceName>')
api.add_resource(DeleteAllUserDevices, '/deleteAll')