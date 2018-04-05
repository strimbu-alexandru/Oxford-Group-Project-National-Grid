from flask import Blueprint, render_template

Index = Blueprint('Index',__name__, template_folder='templates', static_folder='static')

# Render the homepage
@Index.route('/')
def home():
	return render_template('index.html')
