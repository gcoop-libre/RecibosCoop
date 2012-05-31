from flask import Flask
from flask import render_template
from pdf import to_pdf
app = Flask(__name__)
app.debug = True
@app.route("/")
@to_pdf
def recibo():
    return render_template("recibo.html")

if __name__ == "__main__":
    app.run()
