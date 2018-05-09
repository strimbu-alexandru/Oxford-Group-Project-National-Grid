import atexit
from datetime import *
from flask import Blueprint
from flask_restful import Resource, Api
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

from app.api.Scheduling import schedulingMethods
from app.Models import ChargingSlot
from app.Database import db_session

# Start scheduler and register the jobs.
def initScheduler():
    # Get the scheduler
    scheduler = BackgroundScheduler()

    # Find the next perfect half hour to start the slot clean up on
    from datetime import datetime, timedelta
    start = datetime.now() + (datetime.min - datetime.now()) % timedelta(minutes=30)

    # Add slot clean up job to scheduler
    scheduler.add_job(
        func = slotCleanUp.cleanUp,
        trigger = IntervalTrigger(start_date=start, minutes=30),
        id = 'slot_cleanup',
        name = 'Refresh Slots',
        replace_existing = True)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    scheduler.start()


# Function to be called every half hour. Passes through all slots and updates as necessary.
class slotCleanUp():
    content = []

    def cleanUp():
        # Log the time we execute the function
        slotCleanUp.content.append(datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M'))
        # Get all the charging slots
        allSlots = ChargingSlot.query.all()

        # For each slot check it's still optimal and update if not
        for slot in allSlots:
            # Currently always looks ahead 24 hours.
            result = schedulingMethods.bestTimeSlot(24, slot.consumption, slot.timeToCharge)
            optPlugInTime = datetime.strptime(result['data'][0]['plugInTime'], '%Y-%m-%dT%H:%MZ')
            # Check if optimal time is later than current optimal time
            if optPlugInTime > slot.plugInTime:
                slotCleanUp.content.append(
                    'Slot ' + str(slot.slotId) + ' updated from ' +
                    str(slot.plugInTime) + ' to ' + str(optPlugInTime)
                )
                # Update slot to reflect new time
                slot.plugInTime = optPlugInTime
                db_session.commit()


# Define api for checking clean up logs:
SlotCleanUp = Blueprint('SlotCleanUp',__name__, url_prefix='/slotCleanUp', template_folder='templates')
api = Api(SlotCleanUp)

class getLogs(Resource):
    def get(self):
        return slotCleanUp.content

class forceCleanUp(Resource):
    def get(self):
        slotCleanUp.cleanUp()
        return getLogs.get(self)

api.add_resource(getLogs, '/')
api.add_resource(forceCleanUp, '/force')
