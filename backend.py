import string
from random import *
from flask import Flask, Blueprint, render_template

# import api modules
from api.Auth import Auth
from api.Scheduling import Scheduling

app = Flask(__name__)

# Link api modules to main app
app.register_blueprint(Auth)
app.register_blueprint(Scheduling)

# randomly generate the secret key for sessions:
allchar = string.ascii_letters + string.punctuation + string.digits
app.secret_key  = "".join(choice(allchar) for x in range(32))

# Render the homepage
@app.route('/')
def home():
	return render_template('index.html')

if __name__ == "__main__":
	app.run()
