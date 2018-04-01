import string
from random import *
from flask import Flask, url_for, request, render_template, session, escape, redirect, Blueprint
from google.oauth2 import id_token
from google.auth.transport import requests

# Declare blueprint:
Auth = Blueprint('Auth',__name__, url_prefix='/auth', template_folder='templates')

# randomly generate the secret key for sessions:
allchar = string.ascii_letters + string.punctuation + string.digits
Auth.secret_key  = "".join(choice(allchar) for x in range(32))

@Auth.route('/')
def index():
    if 'username' in session:
        return 'Logged in.'
    return 'You are not logged in.'

@Auth.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':

		token = request['idtoken']
		CLIENT_ID = "321008678947-bd2hvj2snrr96if8ec34vvecd2rmmcdk.apps.googleusercontent.com"

		try:
			# Specify the CLIENT_ID of the app that accesses the backend:
			idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

			if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				raise ValueError('Wrong issuer.')

			# ID token is valid. Get the user's Google Account ID from the decoded token.
			userId = idinfo['sub']

		except ValueError:
			# Invalid token
			pass

		# log the user in
		session['username'] = userId
		# send them to a member page --todo: this will presumably be a page dealt with by another part of the app
		return redirect(url_for(Auth.members))
	
	# Invalid token or get request - send to login page
	return (render_template("login_googleOauth.html"))

@Auth.route('/members')
def members():
	if 'username' in session:
		return render_template('member.html')

@Auth.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for(Auth.index))