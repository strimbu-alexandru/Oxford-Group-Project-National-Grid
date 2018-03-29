import requests
import json
import datetime
import time

from flask import Flask
from flask import request
app = Flask(__name__)

headers = {
  'Accept': 'application/json'
}

#this code would get, from the browser, the power of a device and the number of minutes the user wants to use it
#it will give a webpage with the power used, the least carbon produced and the optimal plug-in time

@app.route('/')
def home():
	return render_template('index.html')


@app.route('/server', methods = ['GET', 'POST'])
	
def main():	
	power = float(request.args.get('power', ''))	#get the power of the device
	timeMin = int(request.args.get('timeMin', ''))	#get the number of minutes it should work
	#power = 10
	#timeMin = 135
	kwh = timeMin/60 * power		#compute the energy consumed in that time
	intervals = timeMin//30			#compute the number of 30 minutes intervals
	data = get_data()				#get the data for the next 24h from now
	#return ("<b>" + data['data'][3]['intensity']['index'] + "</b>")
	minCarbon = 1000000
	minCarbonTime = data['data'][0]['from']
	for i in range (0, 48 - intervals):		#go through the data and choose a period with the mionimum carbon consumed
		carbon = 0
		for j in range (0, intervals):
			carbon += data['data'][i + j]['intensity']['forecast'] * power * 0.5
		carbon += data['data'][i + intervals]['intensity']['forecast'] * power * (timeMin - 30 * intervals) / 30 * 0.5
		if carbon < minCarbon:
			minCarbon = carbon
			minCarbonTime = data['data'][i]['from']
	
	return "<html><body>Total energy consumed: " + str(kwh) + " kwh<br>Total Carbon produced: " + str(minCarbon/kwh) + "/kwh</br> Plug-in time: "  + str(minCarbonTime) + "</body></html>"
	
def get_data():		#this finds the current time and returns the data for the next 24h
	currTime = time.strftime("%Y-%m-%dT%H:%MZ")
	link = 'https://api.carbonintensity.org.uk/intensity/' + currTime + '/fw24h'
	r = requests.get(link, params={}, headers = headers)
	data = json.loads(r.text)
	return data

if __name__ == "__main__":
	app.run()
