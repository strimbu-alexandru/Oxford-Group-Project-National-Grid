from google.oauth2 import id_token
from google.auth.transport import requests
from functools import wraps
from flask import Flask, url_for, request, render_template, Blueprint, json, Response, session, redirect
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


# Checks user is logged in. Redirects to login page if not
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if isAuthenticated():
			return f(*args, **kwargs)
		return redirect(url_for('Auth.login'))

	return decorated_function


class Home(Resource):
	@login_required
	def get(self):
		authToken = authMethods.getAuthTokenFromJWT(session['JWT'])
		user = authMethods.findUserByToken(authToken)
		return 'Logged in as ' + user.name

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
	@login_required
	def get(self):
		authToken = authMethods.getAuthTokenFromJWT(session['JWT'])
		
		# End the session
		session.pop('JWT', None)

		# Log user out in database
		user = authMethods.findUserByToken(authToken)
		user = authMethods.logUserOut(user)
		return 'Logged out successfully.'


# Login with username/password
class MobileLogin(Resource):
	def post(self):
		if request.form:

			username = request.form['username']
			password = request.form['password']

			# log the user in on the database
			user = authMethods.findUserByUsername(username)
			
			if user == None:
				return output_html(render_template("login_mobile.html",error = 'User not found - invalid username or password'),200)

			if authMethods.authenticateByPassword(user,password):
				authToken = authMethods.generateToken()				# Get the new token
				user = authMethods.logUserIn(user, authToken)

				# Obtain the JWT to send back to client
				JWToken = authMethods.getJWTfromAuthToken(authToken)

				# Create a session for them
				session['JWT'] = JWToken

				return 'Logged in as: ' + user.name

		return MobileLogin.get(self)

	def get(self):
		# Send to mobile login page
		return output_html(render_template("login_mobile.html"), 200)


class ChangeMobileLogin(Resource):
	@login_required
	def post(self):
		if request.form:
			# Find the user
			authToken = authMethods.getAuthTokenFromJWT(session['JWT'])
			user = authMethods.findUserByToken(authToken)

			# Get info from form
			username = request.form['username']
			password = request.form['password']

			# Update user
			authMethods.setUsernameAndPassword(user,username,password)

			return 'username and password set successfully'

		return ChangeMobileLogin.get(self)

	@login_required
	def get(self):
		return output_html(render_template("login_mobile_change.html"), 200)

class RemoveMobileLogin(Resource):
	@login_required
	def get(self):
		# Find the user
		authToken = authMethods.getAuthTokenFromJWT(session['JWT'])
		user = authMethods.findUserByToken(authToken)

		authMethods.removePassword(user)
		return 'Password access revoked'


api.add_resource(Home, '/')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

# Mobile logins
api.add_resource(MobileLogin, '/mobile/login')
api.add_resource(ChangeMobileLogin, '/mobile/login/edit')
api.add_resource(RemoveMobileLogin, '/mobile/login/remove')
