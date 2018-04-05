from google.oauth2 import id_token
from google.auth.transport import requests
from flask import Flask, url_for, request, render_template, Blueprint, json, Response, session
from flask_restful import Resource, Api

from app.api.AuthMethods import authMethods
isAuthenticated = authMethods.isAuthenticated

Auth = Blueprint('Auth',__name__, url_prefix='/auth', template_folder='templates')
api = Api(Auth)

# Client ID to authenticate with google
CLIENT_ID = '395319603732-s2ictf4jgnfj5c7ra1dm64oatnrmebqf.apps.googleusercontent.com'	#team10 account

# For rendering the webpages
def output_html(data, code, headers=None):
    resp = Response(data, mimetype='text/html', headers=headers)
    resp.status_code = code
    return resp

class Home(Resource):
	def get(self):
		if isAuthenticated():
			authToken = authMethods.getAuthTokenFromJWT(session['JWT'])
			user = authMethods.findUserByToken(authToken)
			return 'Logged in as ' + user.name
		return Login.get(self)

# Log the user in. Generates a new token each time.
class Login(Resource):
	def post(self):
		if request.form:
			idToken = request.form['idtoken']
			try:
				# Specify the CLIENT_ID of the app that accesses the backend:
				idinfo = id_token.verify_oauth2_token(idToken, requests.Request(), CLIENT_ID)

				if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
					raise ValueError('Wrong issuer.')

			# Invalid token
			except ValueError:
				return 'invalid token'

			userId = str(idinfo['sub'])		# Convert to string so it can be stored correctly in the db
			name   = idinfo['name']

			# log the user in on the database
			user = authMethods.findOrRegisterUser(userId, name)	# Find the user and register if first login
			authToken = authMethods.generateToken()				# Get the new token
			user = authMethods.logUserIn(user, authToken)

			# Obtain the JWT to send back to client
			JWToken = authMethods.getJWTfromAuthToken(authToken)

			# Create a session for them
			session['JWT'] = JWToken

			return 'Logged in as: ' + user.name
		return Login.get(self)

	def get(self):
		# Send to login page
		return output_html(render_template("login_googleOauth.html"), 200)

# Expire current token
class Logout(Resource):
	def get(self):
		if isAuthenticated():
			authToken = authMethods.getAuthTokenFromJWT(session['JWT'])
			
			# End the session
			session.pop('JWT', None)

			# Log user out in database
			user = authMethods.findUserByToken(authToken)
			user = authMethods.logUserOut(user)
			return 'Logged out successfully.'

		return 'User not logged in.'

api.add_resource(Home, '/')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')