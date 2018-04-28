# sqlalchemy declarative
from datetime import *
from collections import OrderedDict
from sqlalchemy import Column, String, DateTime, Integer, Interval, ForeignKey, UniqueConstraint

from app.Database import Base

# Basic serialiser for models
class DictSerializable(object):
	def _asdict(self):
		result = OrderedDict()
		for key in self.__mapper__.c.keys():
			value = getattr(self, key)
			if type(value) is datetime:
				value = value.strftime('%Y-%m-%d %H:%M')
			result[key] = value
		return result


# Store the registered users of the app
class User(Base, DictSerializable):
	__tablename__ = 'users'

	userId 			= Column(String(128), primary_key = True)
	name 			= Column(String(128))
	authToken		= Column(String(128), unique = True)
	tokenExpiryDate = Column(DateTime)
	# For use with mobile app:
	username		= Column(String(128), unique = True)
	passwordHash	= Column(String(128))

	def __init__(self, userId=None, name=None, authToken=None, tokenExpiryDate=None):
		self.userId = userId
		self.name = name
		self.authToken = authToken
		self.tokenExpiryDate = tokenExpiryDate
		self.username = userId
		self.passwordHash = ''

	def __repr__(self):
		return '<User %r>' % (self.name)

# Store the device put by the users of the app
# The devices correspond to each user, identified by its id
class UserDevice(Base, DictSerializable):
	__tablename__ = 'userDevices'

	deviceId = Column(Integer, primary_key = True)
	userId = Column(String(128), ForeignKey('users.userId'))
	deviceName = Column(String(128))
	consumption = Column(Integer)
	timeToCharge = Column(Integer)

	__table_args__ = (UniqueConstraint('userId', 'deviceName', name='uniqueConstraint'),)

	def __init__(self, userId = None, deviceName = None, consumption = None, timeToCharge = None):
		self.userId = userId
		self.deviceName = deviceName
		self.consumption = consumption
		self.timeToCharge = timeToCharge


# Store the charging slots for each user
# Each slot links to a device and a user
class ChargingSlot (Base, DictSerializable):
	__tablename__ = 'chargingSlots'

	slotId = Column(Integer, primary_key = True)
	userId = Column(String(128), ForeignKey('users.userId'))
	deviceId = Column(Integer, ForeignKey('userDevices.deviceId'))		# Can be null if device is not registered
	deviceName = Column(Integer)										# Fill these columns for
	consumption = Column(Integer)										# unregistered devices only
	plugInTime = Column(DateTime)
	timeToCharge = Column(Integer)

	def __init__(self, userId=None, deviceId=None, deviceName=None, consumption=None, plugInTime=None, timeToCharge=None):
		self.userId = userId
		self.deviceId = deviceId
		self.deviceName = deviceName
		self.consumption = consumption
		self.plugInTime = plugInTime
		self.timeToCharge = timeToCharge