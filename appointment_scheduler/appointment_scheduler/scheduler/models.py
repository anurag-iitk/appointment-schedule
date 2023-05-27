"""
This documents contains the models related to Appointment schedule for offline verification
"""
from datetime import datetime

from mongoengine import Document, fields, ValidationError
from backend.user.models import User

from datetime import datetime, timedelta
from django.utils import timezone


def is_holiday(date):
    holidays = [
        datetime.date(2023, 1, 1),
        datetime.date(2023, 12, 25)
    ]
    return date in holidays


def validate_slot_time(value):
    value_datetime = datetime.fromtimestamp(value)
    value_date = value_datetime.date()

    if value_datetime.weekday() == 6:  # Sunday
        raise ValidationError("Appointments are not available on Sundays.")

    start_time = value_datetime.replace(hour=10, minute=0, second=0)
    end_time = value_datetime.replace(hour=17, minute=0, second=0)

    if value_datetime < start_time or value_datetime > end_time:
        raise ValidationError("Appointments are available between 10 AM and 5 PM on Monday to Saturday.")
    if value_datetime.minute % 15 != 0:
        raise ValidationError("Appointments must start at a 15-minute interval.")
    if value_datetime.second % 60 != 0:
        raise ValidationError("Appointments must start at a 15-minute interval.")

    if value_date > timezone.now().date() + timedelta(days=10):
        raise ValidationError("Appointments can only be booked for the next 10 days.")


class Appointment(Document):
    slot = fields.IntField(primary=True, required=True, validation=validate_slot_time)
    userId = fields.ReferenceField(User, required=False)
    isBooked = fields.BooleanField(default=False)
    applicationId = fields.StringField(required=False)
