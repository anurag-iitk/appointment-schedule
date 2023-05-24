from django.db import models

from mongoengine import Document, fields, ReferenceField, EmbeddedDocumentField

class Officer(Document):
    userId = fields.StringField(primary_key=True)
    designation = fields.StringField(default="NONE")
    department = fields.StringField(default="NONE")
    zones = fields.ListField(fields.IntField(), default=[])
    roles = fields.ListField(fields.StringField(), required=False)

class User(Document):
    userId = fields.StringField(primary_key=True)
    name = fields.StringField(default="NONE")
    email = fields.SequenceField(default="NONE")



class Appointment(Document):
    doctorid = fields.EmbeddedDocumentField(Officer, required=True)
    userid = fields.EmbeddedDocumentField(User, required=True)
    appointment_time = fields.DateTimeField()
