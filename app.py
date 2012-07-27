# -*- encoding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import jsonify

from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin
from werkzeug import secure_filename
import helpers

from pdf import to_pdf
from num_to_text import Traductor

app = Flask(__name__)
app.config.from_pyfile('config.py')

helpers.Helpers(app)
db = Database(app)
auth = Auth(app, db)
admin = Admin(app, auth)

import models
import forms

@app.route("/")
def principal():
    return render_template("principal.html")

def importar_recibos(fecha, montos):
    socios = [socio for socio in models.Socio.select()]

    for (index, monto) in enumerate(montos):
        retiro = models.Retiro(socio=socios[index], fecha=fecha, monto=monto)
        retiro.save()


@app.route("/importar", methods=["POST", "GET"])
def importar():
    if request.method == 'POST':
        print request.form
        form = forms.ImportarForm(request.form, csrf_enabled=False)

        if form.validate():
            importar_recibos(request.form['fecha'], request.form['montos'].strip().split("\n"))
            return redirect(url_for('principal'))

    else:
        form = forms.ImportarForm(csrf_enabled=False)

    socios = u"\n".join([x + u" → " for x in obtener_lista_de_socios()])
    return render_template("importar.html", form=form, socios=socios)

@app.route("/to_pdf")
@to_pdf()
def recibo():
    return render_template("recibo.html")

@app.route("/pdf/<retiro_id>")
@to_pdf()
def generar_recibo(retiro_id):
    retiro = models.Retiro.get(id=retiro_id)
    cooperativa = {'matricula': 12345, 'cuit': 3333, 'domicilio': 'Velasco 508'}
    traductor = Traductor()
    monto_como_cadena = traductor.to_text(retiro.monto)
    lugar = u"Ciudad Autónoma de Buenos Aires"
    return render_template("recibo.html", cooperativa=cooperativa, retiro=retiro, lugar=lugar, monto_como_cadena=monto_como_cadena)

@app.route("/pdf/mes/<mes>")
def generar_recibo_por_mes(mes):
    pass

@app.route("/obtener_retiros")
def obtener_retiros():
    retiros = models.Retiro.select()
    datos = [convertir_en_formato_de_tabla(d) for d in retiros]
    total = retiros.count()
    # TODO: hacer un filtrado por el parametro search
    # TODO: contar solamentes los que resulten de una busqueda.
    total_vistos = retiros.count()

    return jsonify({
        'aaData': datos,
        'iTotalDisplayRecords': total_vistos,
        'iTotalRecords': total,
    })

def obtener_lista_de_socios():
    socios = models.Socio.select()
    return [x.nombre_completo() for x in socios]

def convertir_en_formato_de_tabla(retiro):
    "Convierte un registro de datos base en una lista de celdas para una tabla."
    nombre = retiro.socio.nombre_completo()
    acciones = "<a href='%s' class='derecha badge badge-warning'>PDF</a>" %(url_for('generar_recibo', retiro_id=retiro.id))
    fecha = retiro.fecha
    return [nombre, fecha, float(retiro.monto), acciones]

if __name__ == "__main__":
    auth.register_admin(admin)
    admin.register(models.Retiro)
    admin.register(models.Socio)
    admin.setup()
    app.run(host="0.0.0.0", processes=2)
