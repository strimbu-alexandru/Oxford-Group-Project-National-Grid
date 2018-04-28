from datetime import *
from flask import Flask, url_for, request, render_template, Blueprint, json, Response, session
from flask_restful import Resource, Api

from app.Models import User, UserDevice, ChargingSlot
from app.api.AuthMethods import authMethods
from app.api.Auth import login_required
from app.Database import db_session


ChargingSlots = Blueprint('ChargingSlots',__name__, url_prefix='/chargingSlots', template_folder='templates')
api = Api(ChargingSlots)

def getUserId():
    #get the userId from User database
    authToken = authMethods.getAuthTokenFromJWT(session['JWT'])
    user = authMethods.findUserByToken(authToken)
    return user.userId

# For use internally to the backend:
class ChargingSlotMethods(Resource):
    # Add a new charging slot for the user and registered device
    def addRegistered(userId, deviceId, plugInTime, timeToCharge):
        chargingSlot = ChargingSlot(deviceId = deviceId, userId = userId, plugInTime = plugInTime, timeToCharge = timeToCharge)
        db_session.add(chargingSlot)
        db_session.commit()
        return chargingSlot

    # Add a charging slot for the user and unregistered device
    def addUnregistered(userId, deviceName, consumption, plugInTime, timeToCharge):
        chargingSlot = ChargingSlot(userId = userId, deviceName = deviceName, consumption = consumption,plugInTime = plugInTime, timeToCharge = timeToCharge)
        db_session.add(chargingSlot)
        db_session.commit()
        return chargingSlot

    # remove given slot
    def removeSlotById(slotId):
        chargingSlot = ChargingSlot.query.filter(ChargingSlot.slotId == slotId).first()
        if chargingSlot == None:
            return 'No such charging slot'
        db_session.delete(chargingSlot)
        db_session.commit()
        return 'Success'

    # remove all slots for given user and device
    def removeSlotByDevice(deviceId, userId):
        chargingSlots = ChargingSlot.query.filter(ChargingSlot.deviceId == deviceId, ChargingSlot.userId == userId).all()
        if chargingSlots == []:
            return 'Nothing to delete for this device'
        for chargingSlot in chargingSlots :
            db_session.delete(chargingSlot)
        db_session.commit()
        return 'Success'

# Add a new charging slot for the user
# require plugInTime as a datetime string with format '%Y-%m-%d %H:%M'
# if deviceId is null, need to supply the device details separately
class AddChargingSlot(Resource):
#    @login_required
    def post(self):
#        userId = getUserId()
        user = User.query.filter(User.name == 'Tiffany Duneau').first()
        userId = user.userId
        # Get data from form
        plugInTime = datetime.strptime(request.form['plugInTime'], '%Y-%m-%d %H:%M')
        timeToCharge = int(request.form['timeToCharge'])
        deviceId = request.form['deviceId']
        deviceName = request.form['deviceName']
        consumption = int(request.form['consumption'])

        if not deviceId == '': # if device is registered
            ChargingSlotMethods.addRegistered(userId, deviceId, plugInTime, timeToCharge)
            return 'success'
        ChargingSlotMethods.addUnregistered(userId, deviceName, consumption, plugInTime, timeToCharge)
        return 'success'

# returns all charging slots for the user that are scheduled for the future
# future: defaults to TRUE - specifies whether to get all slots ever or just upcoming ones
class GetChargingSlots(Resource):
    @login_required
    def get(self, future=True):
        userId = getUserId()
        if future:
            chargingSlots = ChargingSlot.query.filter(ChargingSlot.userId == userId, ChargingSlot.plugInTime > datetime.now()).all()
        else:
            chargingSlots = ChargingSlot.query.filter(ChargingSlot.userId == userId).all()

        # Serialise the charging slots returned.
        def dictify(ChargingSlot):
            return ChargingSlot._asdict()
        chargingSlotsDict = list(map(dictify, chargingSlots))

        return chargingSlotsDict

# Delete specific slot
class DeleteChargingSlot(Resource):
    @login_required
    def get(self, slotId):
        return ChargingSlotMethods.removeSlotById(slotId)

# Delete all slots registered for given device
# If deviceId is set to 'all', deletes all slots associated with user
class DeleteAllChargingSlots(Resource):
    @login_required
    def get(self, deviceId):
        userId = getUserId()
        if deviceId == 'all':
            chargingSlots = ChargingSlot.query.filter(ChargingSlot.userId == userId)
            for chargingSlot in chargingSlots:
                ChargingSlotMethods.removeSlotById(chargingSlot.slotId)
            return 'successfully deleted'
        return ChargingSlotMethods.removeSlotByDevice(deviceId, userId)


api.add_resource(AddChargingSlot, '/add')
api.add_resource(GetChargingSlots, '/get/<future>')
api.add_resource(DeleteChargingSlot, '/delete/<slotId>')
api.add_resource(DeleteAllChargingSlots, '/deleteAll/<deviceId>')