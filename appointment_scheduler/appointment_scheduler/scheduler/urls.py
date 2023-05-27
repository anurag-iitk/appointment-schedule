from django.urls import path
from backend.appointment import views

urlpatterns = [
    path("create", views.create_appointemnt),
    # path("reschedule", views.reschedule_appointment),
    path("getAll", views.get_future_appointments),
]
