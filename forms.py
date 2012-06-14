from flaskext.wtf import Form, TextAreaField, Required

class ImportarForm(Form):
    datos = TextAreaField('Datos', validators=[Required()])

