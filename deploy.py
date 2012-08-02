import os

import inspect
import app
import models
from config import DATABASE
import csv

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


def cargar_coopeativa_con_socios():
    try:
        cooperativas = csv.reader(open('cooperativas.csv', 'rb'), delimiter=',', quotechar='|')

        # Se evita leer la cabecera del archivo
        cooperativas.next()

        for (index, s) in enumerate(cooperativas):
            registro_coop = models.Cooperativa(nombre=s[0], cuit=s[1],
                                      matricula=s[2], domicilio=s[3])
            registro_coop.save()
            print u"Importando cooperativa: %s" %(registro_coop)
    except IOError, e:
        print "Error: no exite el archivo 'cooperativas.csv' (vea el archivo 'tests/data/cooperativas.csv' como ejemplo.)"

    try:
        socios = csv.reader(open('socios.csv', 'rb'), delimiter=',', quotechar='|')

        # Se evita leer la cabecera del archivo
        socios.next()

        for (index, s) in enumerate(socios):
            registro_socio = models.Socio(apellido=s[0], nombre=s[1],
                                          domicilio=s[2], cuit=s[3],
                                          dni=s[4], cooperativa=registro_coop,
                                          numero_asociado=index + 1)
            registro_socio.save()
            print u"Importando socio: %s" %(registro_socio)
    except IOError, e:
        print "Error: no exite el archivo 'socios.csv' (vea el archivo 'tests/data/socios.csv' como ejemplo.)"

if __name__ == '__main__':
    crear_tablas()
    cargar_coopeativa_con_socios()
