import requests
from flask import Flask, url_for, request, render_template, session, escape, redirect, Blueprint
from google.oauth2 import id_token, credentials
from google.auth.transport import requests

# Declare blueprint:
Auth = Blueprint('Auth',__name__, url_prefix='/auth', template_folder='modules/templates')

CLIENT_ID = '395319603732-s2ictf4jgnfj5c7ra1dm64oatnrmebqf.apps.googleusercontent.com'	#team10 account

@Auth.route('/')
def index():
	if 'user' in session:
		return ('Logged in as ' + session['user']['name'])
	return 'You are not logged in.'

@Auth.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		if request.form:
			token = request.form['idtoken']
			try:
				# Specify the CLIENT_ID of the app that accesses the backend:
				idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

				if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
					raise ValueError('Wrong issuer.')

			# Invalid token
			except ValueError:
				return 'invalid token'

			# log the user in on the server
			session['user'] = {
					'userId': idinfo['iss'],
					'name': idinfo['name']
				}

			return session['user']['name']

	# Invalid token or get request - send to login page
	return (render_template("login_googleOauth.html"))

@Auth.route('/logout')
def logout():
	# remove user from session (log them out)
	if 'user' in session:
		session.pop('user', None)
		return 'logged out from server'
	return 'not logged in'
