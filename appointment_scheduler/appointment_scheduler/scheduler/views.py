import json
import logging
from datetime import datetime, timedelta, time

from mongoengine import ValidationError, NotUniqueError
from rest_framework import status

from rest_framework.decorators import api_view

from scheduler.utils import create_pending_slots
from backend.authorization import authenticate
from backend.pdf_service.utils import get_user_name
from backend.services.api_response import ApiResponse, ApiSuccessResponse
from backend.appointment.models import Appointment
from backend.services.utils import get_paginated_data
from backend.userRegistration.enums import UserType
from backend.services.unique_key_generator import UniqueIdGenerator


logger = logging.getLogger(__name__)


@api_view(["POST"])
@authenticate(["USER"])
def create_appointemnt(request):
    userId = request.user_id
    slot = request.data.get("slot")
    application_id = UniqueIdGenerator().get_tdr_application_id()
    appointment = Appointment.objects(slot=slot).first()
    if not appointment:
        return ApiResponse(err="No such slots", status=status.HTTP_200_OK)
    if appointment.isBooked:
        return ApiResponse(err="slot already booked", status=200)
    try:
        appointment = Appointment(slot=slot, userId=userId, isBooked=True, applicationId=application_id)
        appointment.validate()
        appointment.save()
        return ApiSuccessResponse()
    except ValidationError as validation_error:
        logger.debug("Invalid appointment data %s", slot)
        return ApiResponse(err=validation_error.to_dict(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except NotUniqueError as not_unique_error:
        logger.debug("not unique key slot %s", slot)
        return ApiResponse(err="slot already taken")
    except Exception as e:
        logger.exception("unable to save appointment")
        return ApiResponse(exp=e, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["GET"])
@authenticate()
def get_future_appointments(request):
    _end_date = datetime.now() + timedelta(days=10)
    end_date = int(_end_date.timestamp())
    start_date = int(datetime.now().timestamp())
    create_pending_slots()
    if request.user_type == UserType.USER.name:
        appointments = Appointment.objects.filter(slot__gte=start_date, slot__lte=end_date).order_by('slot') \
            .exclude("userId") \
            .exclude("applicationId")
    else:
        appointments = Appointment.objects.filter(slot__gte=start_date, slot__lte=end_date).order_by('slot')

    offset_param = int(request.GET.get('offset', 10))
    page_number = request.GET.get('page', 1)
    paginated_data = get_paginated_data(appointments,
                                        page_number,
                                        'appointments',
                                        offset=offset_param)
    _appointments = []
    for appointment in paginated_data.get("appointments"):
        appointment.pop("_id")
        if request.user_type == UserType.KDA_OFFICER.name:
            user_id = appointment.get("userId")
            if user_id:
                appointment["user"] = get_user_name(user_id)
                appointment.pop('userId')
        _appointments.append(appointment)
    paginated_data["appointments"] = _appointments
    return ApiResponse(paginated_data)

#
# @api_view(['POST'])
# def reschedule_appointment(request, appointment_id):
#     appointment_date = request.data.get('appointmentDate')
#     appointment_time = request.data.get('appointmentTime')
#
#     try:
#         appointment = Appointment.objects.get(id=appointment_id)
#     except ValidationError as e:
#         return ApiResponse(err="Appointment not found", status=status.HTTP_400_BAD_REQUEST)
#
#     appointment_datetime = datetime.combine(appointment_date, appointment_time)
#     if is_holiday(appointment_datetime.date()) or is_weekend(appointment_datetime.date()) or not is_valid_time(
#             appointment_time):
#         return ApiResponse(err="Appintment cannot be scheduled on a holiday", status=status.HTTP_400_BAD_REQUEST)
#
#     # check if the appoinmtmet has already been rescheduled twice
#     if appointment.rescheduleCount >= 2:
#         return ApiResponse(err="Appointment rescheduling limit reached", status=status.HTTP_400_BAD_REQUEST)
#
#     # update appointment details
#     appointment.appointmentDate = appointment_date
#     appointment.appointmentTime = appointment_time
#     appointment.rescheduleCount += 1
#     appointment.save()
#
#     return ApiResponse(msg="Appointment rescheduled successfully")
