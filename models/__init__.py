from peewee import *
from app import db


class Socio(db.Model):

    numero_asociado = IntegerField()
    apellido = CharField(max_lenght=255)
    nombre = CharField(max_lenght=255)
    domicilio = TextField()
    cuit = CharField(max_length=255)
    dni = CharField(max_length=255)

    def __unicode__(self):
        return u'<Socio %s %s>' % (self.nombre, self.apellido)

class Retiro(db.Model):

    monto = DecimalField(max_digits=30, decimal_places=2)
    fecha = CharField()
    socio = ForeignKeyField(Socio, related_name="retiros")

    def __unicode__(self):
        return u'<Retiro %s de %s$ Socio %s %s>' % (
                                        self.fecha,
                                        self.monto,
                                        self.socio.nombre,
                                        self.socio.apellido
                                        )

