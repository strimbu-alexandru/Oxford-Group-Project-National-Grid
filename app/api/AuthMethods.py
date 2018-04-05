import string
from random import *
from datetime import *
from ast import literal_eval
from jwcrypto import jwt, jwk, jwe
from flask import request, session, url_for, redirect
from jwcrypto.common import json_encode, json_decode

from app.Models import User
from app.Database import db_session
from app.ErrorHandler import CustomError
from config import Config


# Defines methods for use in the auth api
class authMethods():

	key = jwk.JWK(generate='oct', size=256)

	# Add new user to the database if not in already. Searches by Id. Returns the user entry on success.
	def findOrRegisterUser(userId,name):
		user = User.query.filter(User.userId == userId).first()
		if user == None:
			# Create a new Entry in the database for the user
			user = User(userId=userId, name=name, authToken='', tokenExpiryDate=datetime.min)
			db_session.add(user)
			db_session.commit()
		
		return user

	def findUserByToken(authToken):
		user = User.query.filter(User.authToken == authToken).first()
		if user == None:
			raise CustomError(authToken + ': user not found', 600)
		return user

	# Updates authToken and tokenExpiryDate for given user and token
	def logUserIn(user, authToken):
		# Set how long the token is valid for
		tokenValidityDuration = timedelta(hours=12)
		tokenExpiryDate = datetime.now() + tokenValidityDuration

		# Update the user record in the database
		user.authToken = authToken
		user.tokenExpiryDate = tokenExpiryDate
		db_session.commit()

		return user

	# Expires user token
	def logUserOut(user):
		user.tokenExpiryDate = datetime.min
		db_session.commit()

		return user

	# Check given token is valid
	def checkValidity(authToken):
		user = authMethods.findUserByToken(authToken)
		if datetime.now() < user.tokenExpiryDate:
			return True
		return False 

	# Check client is authenticated
	def isAuthenticated():
		if 'JWT' in session:
			authToken = authMethods.getAuthTokenFromJWT(session['JWT'])
			if authMethods.checkValidity(authToken):
				return True
		return False

	# Generate a random token for the user
	# Prefix with the time it is generated at to ensure uniqeness
	def generateToken():
		now = datetime.now()
		token = now.strftime("%d/%m/%Y %H:%M:%S ") + "".join(choice(string.ascii_letters + string.digits) for x in range(90))
		return token

	# Create a JWT with server generated token as content to send to client
	def getJWTfromAuthToken(authToken):
		# Get the key
		key = Config.JWT_KEY

		# Define headers and claims
		header = {"alg": "HS512"}
		claims = {"authToken": authToken}

		# Create signed token
		token = jwt.JWT(header, claims)
		token.make_signed_token(key)
		signedToken = token.serialize(compact = True)

		# Encrypt token
		eprot={"alg": "A256KW", "enc": "A256CBC-HS512"}
		Etoken = jwe.JWE(signedToken, json_encode(eprot))
		Etoken.add_recipient(key)
		encryptedSignedToken = Etoken.serialize(compact = True)

		return encryptedSignedToken

	def getAuthTokenFromJWT(JWEtoken):
		# Get the key
		key = Config.JWT_KEY

		# Decrypt token
		encryptedSignedToken = jwt.JWT(jwt=JWEtoken).token
		encryptedSignedToken.decrypt(key)
		raw_payload = encryptedSignedToken.payload
		JWStoken = raw_payload.decode("utf-8")

		# extract payload from signed token
		signedToken = jwt.JWT(jwt=JWStoken).token
		signedToken.verify(key)
		payload = json_decode(signedToken.payload)
		authToken = payload['authToken']

		return authToken
