from flask import Flask
from flask import render_template
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin
from pdf import to_pdf

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = Database(app)
auth = Auth(app, db)
admin = Admin(app, auth)


import models

@app.route("/")
def principal():
    return render_template("principal.html")

@app.route("/to_pdf")
@to_pdf
def recibo():
    return render_template("recibo.html")

if __name__ == "__main__":
    auth.register_admin(admin)
    admin.setup()

    app.run()
