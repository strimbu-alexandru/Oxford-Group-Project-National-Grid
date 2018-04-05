# sqlalchemy declarative

from sqlalchemy import Column, String, DateTime
from app.Database import Base

# Store the registered users of the app
class User(Base):
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
class UserDevices(Base):
	__tablename__ = 'userDevices'
	
	userId = Column(String(128), primary_key = True)
	deviceName = Column(String(128))
	consumption = Column(Int)
	timeToCharge = Column(Int)
	
	def __init__(self, userId = None, deviceName = None, consumption = None, timeToCharge = None):
		self.userId = userId
		self.deviceName = deviceName
		self.consumption = consumption
		self.timeToCharge = timeToCharge
