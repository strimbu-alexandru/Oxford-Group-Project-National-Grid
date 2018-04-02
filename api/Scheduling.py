import requests
import json
import datetime
import time

from flask import Flask, Blueprint, render_template, request, jsonify
from flask_restful import Resource, Api

Scheduling = Blueprint('Scheduling',__name__, template_folder='templates')
api = Api(Scheduling)

headers = {
  'Accept': 'application/json'
}

#this code would get, from the browser, the power of a device and the number of minutes the user wants to use it
#it will give a webpage with the power used, the least carbon produced and the optimal plug-in time
@Scheduling.route('/server', methods = ['GET', 'POST'])

class BestTime24h(Resource):
	def get_data():		#this finds the current time and returns the data for the next 24h
		currTime = time.strftime("%Y-%m-%dT%H:%MZ")
		link = 'https://api.carbonintensity.org.uk/intensity/' + currTime + '/fw24h'
		r = requests.get(link, params={}, headers = headers)
		data = json.loads(r.text)
		return data
	
	def get(self, powerGET, timeMinGET):	
		power = float(powerGET)			#get the power of the device
		timeMin = int(timeMinGET)		#get the number of minutes it should work
		#power = 10
		#timeMin = 135
		kwh = timeMin/60 * power		#compute the energy consumed in that time
		intervals = timeMin//30			#compute the number of 30 minutes intervals
		data = BestTime24h.get_data()	#get the data for the next 24h from now
		minCarbon = 1000000
		minCarbonTime = data['data'][0]['from']
		for i in range (0, 48 - intervals):		#go through the data and choose a period with the minimum carbon consumed
			carbon = 0
			for j in range (0, intervals):
				carbon += data['data'][i + j]['intensity']['forecast'] * power * 0.5
			carbon += data['data'][i + intervals]['intensity']['forecast'] * power * (timeMin - 30 * intervals) / 30 * 0.5
			if carbon < minCarbon:
				minCarbon = carbon
				minCarbonTime = data['data'][i]['from']
		result = {'data': [{'enrgyConsumed': str(kwh)}, {'carbonProduced': str(minCarbon/kwh)}, {'plugInTime': str(minCarbonTime)}]}
		return jsonify(result)	#return a json with the data

api.add_resource(BestTime24h, '/server/best24h/<powerGET>/<timeMinGET>')
