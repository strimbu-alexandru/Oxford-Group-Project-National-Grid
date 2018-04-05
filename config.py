import string
from random import *
from jwcrypto import jwk

class Config(object):

	# Databse stuff
	SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://team10:team10database@team10.mysql.pythonanywhere-services.com/team10$database"
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Auth secret key
	SECRET_KEY  = "".join(choice(string.ascii_letters + string.punctuation + string.digits) for x in range(32))

	# Key for use with JWT
	JWT_KEY = jwk.JWK(generate='oct', size=256)
