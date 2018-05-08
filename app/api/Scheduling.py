import requests
import json
import datetime
import time

from flask import Flask, Blueprint, render_template, request, jsonify
from flask_restful import Resource, Api

Scheduling = Blueprint('Scheduling', __name__, template_folder='templates')
api = Api(Scheduling)

headers = {
    'Accept': 'application/json'
}


# this code would get, from the browser, the power of a device and the number of minutes the user wants to use it
# it will give a webpage with the power used, the least carbon produced and the optimal plug-in time
@Scheduling.route('/server', methods=['GET', 'POST'])

class BestTime24h(Resource):
    def get(self, powerGET, timeMinGET):
        result = schedulingMethods.bestTimeSlot(24, float(powerGET), int(timeMinGET))
        return jsonify(result)  # return a json with the data

class BestTime48h(Resource):
    def get(self, powerGET, timeMinGET):
        result = schedulingMethods.bestTimeSlot(48, float(powerGET), int(timeMinGET))
        return jsonify(result)  # return a json with the data

api.add_resource(BestTime24h, '/server/best24h/<powerGET>/<timeMinGET>')
api.add_resource(BestTime48h, '/server/best48h/<powerGET>/<timeMinGET>')


# Code that does the work. In a class so it is available internally to other parts of the back end.
class schedulingMethods():
    def get_data(lookAheadTime):  # this finds the current time and returns the data for the next fwTime hours
        currTime = time.strftime("%Y-%m-%dT%H:%MZ")
        link = 'https://api.carbonintensity.org.uk/intensity/' + currTime + '/fw' + str(lookAheadTime) + 'h'
        r = requests.get(link, params={}, headers=headers)
        data = json.loads(r.text)
        return data

    def bestTimeSlot(lookAheadTime, power, timeMin):
        kwh = timeMin / 60 * power  # compute the energy consumed in that time
        intervals = timeMin // 30  # compute the number of 30 minutes intervals
        data = schedulingMethods.get_data(lookAheadTime)  # get the data for the next 24h from now
        minCarbon = 1000000
        minCarbonTime = data['data'][0]['from']
        size = len(data['data'])
        for i in range(0, size - intervals):  # go through the data and choose a period with the minimum carbon consumed
            carbon = 0
            for j in range(0, intervals):
                carbon += data['data'][i + j]['intensity']['forecast'] * power * 0.5
            carbon += data['data'][i + intervals]['intensity']['forecast'] * power * (timeMin - 30 * intervals) / 30 * 0.5
            if carbon < minCarbon:
                minCarbon = carbon
                minCarbonTime = data['data'][i]['from']
        carbonNow = 0
        for i in range(0, intervals):  # compute carbon produced if plugged-in now
            carbonNow += data['data'][i]['intensity']['forecast'] * power * 0.5
        carbonNow += data['data'][i + intervals]['intensity']['forecast'] * power * (timeMin - 30 * intervals) / 30 * 0.5
        carbonRed = carbonNow - minCarbon
        # note that the carbon produced is in g/kwh, but the carbon reduced is in g (so no need to multiply with kwh)
        return {
            'data': [{
                'energyConsumed': str(kwh),
                'carbonProduced': str(minCarbon / kwh),
                'plugInTime': str(minCarbonTime),
                'carbonReduced': str(carbonRed)
            }]
        }