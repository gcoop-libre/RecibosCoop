from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin
from werkzeug import secure_filename

from pdf import to_pdf

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = Database(app)
auth = Auth(app, db)
admin = Admin(app, auth)


import models
import forms

@app.route("/", methods=("GET", "POST"))
def principal():
    form = forms.EntradaForm(csrf_enabled=False)

    if form.validate_on_submit():
        filename = secure_filename(form.data['archivo'].filename)
        # filename tiene la ruta al archivo completo
        # redirect

    return render_template("principal.html", form=form)

@app.route("/procesar")
def procesar():

    pass

@app.route("/to_pdf")
@to_pdf
def recibo():
    return render_template("recibo.html")

if __name__ == "__main__":
    auth.register_admin(admin)
    admin.setup()

    app.run()
