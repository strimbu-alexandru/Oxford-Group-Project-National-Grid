# sqlalchemy declarative

from collections import OrderedDict
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, UniqueConstraint

from app.Database import Base

# Basic serialiser for models
class DictSerializable(object):
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


# Store the registered users of the app
class User(Base, DictSerializable):
	__tablename__ = 'users'

	userId 			= Column(String(128), primary_key = True)
	name 			= Column(String(128))
	authToken		= Column(String(128), unique = True)
	tokenExpiryDate = Column(DateTime)

	def __init__(self, userId=None, name=None, authToken=None, tokenExpiryDate=None):
		self.userId = userId
		self.name = name
		self.authToken = authToken
		self.tokenExpiryDate = tokenExpiryDate

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
	
	__table_args__ = (UniqueConstraint('userId', 'deviceName', name = 'uniqueConstraint'),)
	
	def __init__(self, userId = None, deviceName = None, consumption = None, timeToCharge = None):
		self.userId = userId
		self.deviceName = deviceName
		self.consumption = consumption
		self.timeToCharge = timeToCharge
