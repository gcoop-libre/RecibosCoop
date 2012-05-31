from peewee import *
from app import db

class Retiro(db.Model):
    monto = IntegerField()
