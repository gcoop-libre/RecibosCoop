import os

import inspect
import app
import models
from config import DATABASE

def crear_tablas():
    if os.path.exists(DATABASE['name']):
        print 'Creando el archivo ' + DATABASE['name']
        os.remove(DATABASE['name'])

    def es_un_modelo(clase):
        return inspect.isclass(clase) and issubclass(clase, models.db.Model)

    for nombre, clase in [(n, c) for n, c in inspect.getmembers(models) if es_un_modelo(c)]:
        clase.create_table(fail_silently=True)
        print 'Creando tabla para el modulo: ' + nombre

    #Crear usuario admin
    app.auth.User.create_table(fail_silently=True)
    admin = app.auth.User(username='admin', admin=True, active=True)
    admin.set_password('admin')
    admin.save()
    print "Creando al usuario administrador."

def cargar_fixture_2_usuarios():
    s1 = models.Socio()
    s1.numero_asociado = 1
    s1.appellido = "Grillo"
    s1.nombre = "Pepe"
    s1.save()
    pass

def cargar_fixture_socios():
    print "Creando socio Hugo Ruscitti"
    s1 = models.Socio(appellido="Ruscitti", nombre="Hugo")
    s1.save()
    s2 = models.Retiro(socio=s1, fecha="123", monto=1234.123)
    s2.save()


if __name__ == '__main__':
    crear_tablas()
    cargar_fixture_socios()
