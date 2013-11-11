# -*- coding: utf-8 -*-

import helpers
import time
import os

from flask import Flask, render_template, redirect, url_for, request, jsonify, abort, send_from_directory

from peewee import Q
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin

from pdf import to_pdf, Pdf
from num_to_text import Traductor

app = Flask(__name__)
app.config.from_pyfile('config.py')

helpers.Helpers(app)
db = Database(app)
auth = Auth(app, db)
admin = Admin(app, auth)


import models
import forms

def menu(opcion):
    opciones = [
            ['/', 'Principal', ''],
            ['/importar', 'Importar', ''],
            ['/admin', 'Administrar', ''],
    ]

    opciones[opcion][2] = 'active'
    return opciones


@app.route("/")
@auth.login_required
def principal():
    return render_template("principal.html", menu=menu(0))

def importar_recibos(fecha, concepto, montos):
    socios = [socio for socio in models.Socio.select()]

    for (index, monto) in enumerate(montos):
        if monto:
            retiro = models.Retiro(socio=socios[index], concepto=concepto, fecha=fecha, monto=monto)
            retiro.save()


@app.route("/importar", methods=["POST", "GET"])
@auth.login_required
def importar():
    if request.method == 'POST':
        form = forms.ImportarForm(request.form, csrf_enabled=False)

        if form.validate():
            fecha = request.form['fecha']
            importar_recibos(fecha, request.form['concepto'], request.form['montos'].strip().split("\n"))
            return redirect(url_for('principal', s=fecha))

    else:
        form = forms.ImportarForm(csrf_enabled=False)

    socios = u"\n".join([x + u" → " for x in obtener_lista_de_socios()])
    return render_template("importar.html", form=form, socios=socios, menu=menu(1))




@app.route("/pdf/<retiro_id>")
@auth.login_required
@to_pdf()
def generar_recibo(retiro_id):
    return generar_recibo_html(retiro_id)

@app.route("/html/<retiro_id>")
@auth.login_required
def generar_recibo_html(retiro_id):
    retiro = models.Retiro.get(id=retiro_id)
    monto_como_cadena = Traductor().to_text(retiro.monto)

    return render_template("recibo.html", cooperativa=retiro.socio.cooperativa, retiro=retiro, monto_como_cadena=monto_como_cadena)


@app.route("/pdf_concatenado", methods=["POST"])
@auth.login_required
def generar_pdf_concatenado():
    id_retiros = request.form.to_dict(False).get('recibo')
    if id_retiros:
        retiros = models.Retiro.select().where(id__in = id_retiros)
        to_text = Traductor().to_text
        pdf = Pdf()

        for retiro in retiros:
            html = render_template("recibo.html", cooperativa=retiro.socio.cooperativa, retiro=retiro, monto_como_cadena=to_text(retiro.monto))
            pdf.append(html)

        titulo = "recibos_agrupados_%s.pdf" % (retiro.fecha_como_string())

        nombre_archivo = os.path.join(app.config['UPLOAD_FOLDER'], titulo)
        archivo_temporal = open(nombre_archivo, 'wb')
        archivo_temporal.write(pdf.get_stream())
        archivo_temporal.close()

        return jsonify(name=titulo)
    else:
        abort(404)


@app.route("/zip_contenedor", methods=["POST"])
@auth.login_required
def generar_zip_contenedor():
    archivos_pdf_generados = []
    id_retiros = request.form.to_dict(False).get('recibo')

    if id_retiros:
        retiros = models.Retiro.select().where(id__in=id_retiros)
        to_text = Traductor().to_text

        for retiro in retiros:
            pdf = Pdf()
            html = render_template("recibo.html", cooperativa=retiro.socio.cooperativa, retiro=retiro, monto_como_cadena=to_text(retiro.monto))
            pdf.append(html)

            titulo = models.Retiro.obtener_nombre_por_id(retiro.id)
            nombre_archivo = os.path.join(app.config['UPLOAD_FOLDER'], titulo + ".pdf")

            archivos_pdf_generados.append(nombre_archivo)
            archivo_temporal = open(nombre_archivo, 'wb')
            archivo_temporal.write(pdf.get_stream())
            archivo_temporal.close()

        import zipfile

        nombre = "recibos_agrupados_%s.zip" %(retiro.fecha_como_string())
        nombre_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre)
        zip = zipfile.ZipFile(nombre_archivo, mode='w')

        for nombre_pdf in archivos_pdf_generados:
          print "zipeando", [nombre_pdf]
          zip.write(nombre_pdf)

        zip.close()

        return jsonify(name=nombre)
    else:
        abort(404)

@app.route("/descargar/<nombre>")
def descargar(nombre):
    return send_from_directory(app.config['UPLOAD_FOLDER'], nombre)

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

    indice_columna_ordenamiento = int(request.args.get('iSortCol_0'))

    # Intenta ordenar los resultados en base a la seleccion del usuario
    if indice_columna_ordenamiento > 0:
        columnas = {
                1: 'apellido',
		2: 'numero',
                3: 'fecha',
                4: 'monto',
                }
        columna_a_ordenar = columnas[indice_columna_ordenamiento]
        tipo_ordenamiento = request.args.get('sSortDir_0')
        retiros = retiros.order_by((columna_a_ordenar, tipo_ordenamiento))
    else:
        retiros = retiros.order_by(('numero', 'desc'))

    retiros = retiros.paginate((desde/limite) + 1, limite)

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
    acciones = [
        "<a href='%s' class='derecha badge badge-warning'>PDF</a>" %(url_for('generar_recibo', retiro_id=retiro.id)),
    ]
    fecha = retiro.fecha
    return [check, nombre, retiro.numero, fecha, "{0:.2f}".format(float(retiro.monto)), ' '.join(acciones)]

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
