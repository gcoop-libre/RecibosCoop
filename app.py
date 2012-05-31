from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def recibo():
    return render_template("recibo.html")

if __name__ == "__main__":
    app.run()
