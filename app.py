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

@app.route("/importar")
def retornos():
    return "retiros"

@app.route("/importar", methods=["POST"])
def importar():
    if request.method == 'POST':
        form = forms.ImportarForm(request.form, csrf_enabled=False)

        if form.validate():
            # Procesar

            # Tal vez con algun filtro para ver los datos recien importados?
            return redirect(url_for('principal'))

    else:
        form = forms.ImportarForm(csrf_enabled=False)

    return render_template("importar.html", form=form)

@app.route("/procesar", methods=["POST"])
def importar_procesar():
    form = forms.EntradaForm(csrf_enabled=False)

    if form.validate_on_submit():
        filename = secure_filename(form.data['archivo'].filename)

    return render_template("procesar.html", filename=filename)

@app.route("/procesar")
def procesar():
    pass

@app.route("/to_pdf")
@to_pdf()
def recibo():
    return render_template("recibo.html")

@app.route("/pdf/<retiro_id>")
@to_pdf()
def generar_recibo(retiro_id):
    return render_template("recibo.html")

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

def convertir_en_formato_de_tabla(retiro):
    "Convierte un registro de datos base en una lista de celdas para una tabla."
    nombre = retiro.socio.nombre
    acciones = "<a href='%s'>imprimir</a>" %(url_for('generar_recibo', retiro_id=retiro.id))
    return [nombre, acciones]

if __name__ == "__main__":
    auth.register_admin(admin)
    admin.register(models.Retiro)
    admin.register(models.Socio)
    admin.setup()
    app.run(processes=2)
