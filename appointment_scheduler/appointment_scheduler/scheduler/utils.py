from datetime import datetime, timedelta
import logging
from backend.appointment.models import Appointment

logger = logging.getLogger(__name__)
"""
Util files for creation of time stamp
It is assumed that all the timestamp of the day are generated at once

"""

def generate_appointment_slots_for_date(start_date):
    appointment_slots = []
    for hour in range(10, 17):  # Available hours from 10 AM to 5 PM
        for minute in range(0, 60, 15):  # 15-minute slots
            slot = datetime.combine(start_date, datetime.min.time()) + timedelta(hours=hour, minutes=minute)
            try:
                appointment = Appointment(slot=int(slot.timestamp()))
                appointment.save()
            except Exception as e:
                logger.exception("unable to save create appointment")
                raise e
    return appointment_slots


def generate_appointment_slots(start_date):
    """
    Generates the empty time slots from the last created appointment
    Appointment slots are always createed for the entire day, hence no need for checking
    :param start_date:
    :return:
    """
    end_date = datetime.now().date() + timedelta(days=10)
    appointment_slots = []
    current_date = start_date

    while current_date <= end_date:
        # Check if the current date is Sunday
        if current_date.weekday() != 6:  # Sunday
            appointment_slots.extend(generate_appointment_slots_for_date(current_date))
        current_date += timedelta(days=1)



def create_pending_slots():
    """
    Generates all the pending slots.
    Fetches the last slot already created,
    and creates pending slots in 10 day window
    :return:
    """
    last_slot = Appointment.objects.order_by('-slot').limit(1)
    last_date = datetime.fromtimestamp(last_slot[0].slot).date()
    from_date = last_date + timedelta(days=1)
    generate_appointment_slots(from_date)


def create_time_slots_for_hour(date, hour):
    start_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour)
    end_time = start_time + timedelta(hours=1)
    time_slots = []

    current_time = start_time
    while current_time < end_time:
        time_slots.append(current_time)
        current_time += timedelta(minutes=15)

    return time_slots


def generate_timestamps_for_day(date):
    """
    Generates timestamps for a given day
    :param date:
    :return:
    """
    timestamps = []
    for hour in range(10, 17):  # Available hours from 10 AM to 5 PM
        time_slots = create_time_slots_for_hour(date, hour)
        timestamps.extend([time_slot.timestamp() for time_slot in time_slots])
    return timestamps
