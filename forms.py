from flaskext.wtf import Form, FileField

class EntradaForm(Form):
   archivo = FileField("Archivo")
