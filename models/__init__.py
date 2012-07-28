from peewee import *
from app import db

class Cooperativa(db.Model):

    cuit = CharField(max_lenght=255)
    nombre = CharField(max_lenght=255)
    matricula = CharField(max_lenght=255)
    domicilio = CharField(max_lenght=255)

    def __unicode__(self):
        return u'<Cooperativa %s>' %(self.nombre)

class Socio(db.Model):

    numero_asociado = IntegerField()
    apellido = CharField(max_lenght=255)
    nombre = CharField(max_lenght=255)
    domicilio = TextField()
    cuit = CharField(max_length=255)
    dni = CharField(max_length=255)
    cooperativa = ForeignKeyField(Cooperativa, related_name="socios")

    def __unicode__(self):
        return u'<Socio %s %s>' % (self.nombre, self.apellido)

    def nombre_completo(self):
        return u"%s %s" %(self.nombre, self.apellido)

class Retiro(db.Model):

    socio = ForeignKeyField(Socio, related_name="retiros")
    fecha = CharField()
    monto = DecimalField(max_digits=30, decimal_places=2)

    def __unicode__(self):
        return u'<Retiro %s de %s$ del socio %s %s>' % (
                                        self.fecha,
                                        self.monto,
                                        self.socio.nombre,
                                        self.socio.apellido
                                        )

