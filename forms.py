from flaskext.wtf import Form, TextAreaField, Required, DateField

class ImportarForm(Form):
    montos = TextAreaField('Montos a retirar', validators=[Required()])
    fecha = DateField("Fecha", validators=[Required()])
