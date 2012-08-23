# -*- coding: utf-8 -*-

import helpers
import time

from flask import Flask, render_template, redirect, url_for, request, Response, jsonify, flash

from peewee import Q
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin
from flask.ext.celery import Celery
from celery import exceptions

from pdf import to_pdf, Pdf
from num_to_text import Traductor

app = Flask(__name__)
app.config.from_pyfile('config.py')

helpers.Helpers(app)
db = Database(app)
auth = Auth(app, db)
admin = Admin(app, auth)
celery = Celery(app)


import models
import forms


@app.route("/")
@auth.login_required
def principal():
    return render_template("principal.html")

def importar_recibos(fecha, montos):
    socios = [socio for socio in models.Socio.select()]

    for (index, monto) in enumerate(montos):
        retiro = models.Retiro(socio=socios[index], fecha=fecha, monto=monto)
        retiro.save()


@app.route("/importar", methods=["POST", "GET"])
@auth.login_required
def importar():
    if request.method == 'POST':
        form = forms.ImportarForm(request.form, csrf_enabled=False)

        if form.validate():
            fecha = request.form['fecha']
            importar_recibos(fecha, request.form['montos'].strip().split("\n"))
            return redirect(url_for('principal', s=fecha))

    else:
        form = forms.ImportarForm(csrf_enabled=False)

    socios = u"\n".join([x + u" → " for x in obtener_lista_de_socios()])
    return render_template("importar.html", form=form, socios=socios)


@app.route("/pdf/<retiro_id>")
@auth.login_required
@to_pdf()
def generar_recibo(retiro_id):
    retiro = models.Retiro.get(id=retiro_id)
    monto_como_cadena = Traductor().to_text(retiro.monto)

    return render_template("recibo.html", cooperativa=retiro.socio.cooperativa, retiro=retiro, monto_como_cadena=monto_como_cadena)


@app.route("/pdf_concatenado", methods=["POST"])
@auth.login_required
def generar_pdf_concatenado():

    id_retiros = request.form.to_dict(False).get('recibo')
    if id_retiros:
        retiros = models.Retiro.select().where(id__in = id_retiros)
        to_text =Traductor().to_text
        pdf = Pdf()
        for retiro in retiros:
            html = render_template("recibo.html", cooperativa=retiro.socio.cooperativa, retiro=retiro, monto_como_cadena=to_text(retiro.monto))
            pdf.append(html)

        resp = Response(pdf.get_stream(), mimetype='application/pdf')
        titulo = "Recibos_concat_%s" % int(time.time())
        resp.headers['Content-Disposition'] = 'attachment; filename="%s.pdf"' %titulo

        return resp
    else:
        flash(u"No seleccionó ninguna fila para generar el PDF", "alert")
        return redirect(url_for('principal'))


def parece_fecha(palabra):
    return '/' in palabra or palabra.isdigit()


@app.route("/obtener_retiros")
def obtener_retiros():
    retiros = models.Retiro.select()

    # Parametros
    campos_de_busqueda = request.args.get('sSearch').split(" ")

    for palabra in campos_de_busqueda:
        if parece_fecha(palabra):
            retiros = retiros.where(fecha__icontains=palabra)
        else:
            condicion_de_busqueda = Q(nombre__icontains=palabra) | Q(apellido__icontains=palabra)
            retiros = retiros.where().join(models.Socio).where(condicion_de_busqueda)

    # Aplicando limites
    limite = int(request.args.get('iDisplayLength'))
    desde = int(request.args.get('iDisplayStart'))
    retiros = retiros.order_by(('fecha', 'desc')).paginate(desde/limite, limite)

    datos = [convertir_en_formato_de_tabla(d) for d in retiros]
    total = retiros.count()

    total_vistos = retiros.count()

    return jsonify({
        'aaData': datos,
        'iTotalDisplayRecords': total_vistos,
        'iTotalRecords': total,
    })

def obtener_lista_de_socios():
    socios = models.Socio.select().order_by('numero_asociado')
    return [x.nombre_completo() for x in socios]

def convertir_en_formato_de_tabla(retiro):
    "Convierte un registro de datos base en una lista de celdas para una tabla."
    nombre = retiro.socio.nombre_completo()
    check = '<input class="centrar selector_recibo" type="checkbox" name="recibo" value="%s">' % retiro.id
    acciones = "<a href='%s' class='derecha badge badge-warning'>PDF</a>" %(url_for('generar_recibo', retiro_id=retiro.id))
    fecha = retiro.fecha
    return [check, nombre, fecha, float(retiro.monto), acciones]

def registrar_modelos(admin, models):
    auth.register_admin(admin)

    for m in ['Retiro', 'Socio', 'Cooperativa']:
        modelo = getattr(models, m, None)

        if modelo:
            admin.register(modelo)

    admin.setup()


if __name__ == '__main__':
    registrar_modelos(admin, models)
    app.run(host="0.0.0.0", port=5000, processes=2)
else:
    registrar_modelos(admin, models)
