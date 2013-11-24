from flaskext.wtf import Form, TextAreaField, Required, DateField, TextField

class ImportarForm(Form):
    montos = TextAreaField('Montos a retirar', validators=[Required()])
    concepto = TextField('Concepto', validators=[Required()])
    fecha = DateField("Fecha", format='%d/%m/%Y', validators=[Required()])
