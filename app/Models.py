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