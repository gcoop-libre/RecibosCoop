from flaskext.wtf import Form, TextAreaField, Required

class ImportarForm(Form):
    montos = TextAreaField('Montos a retirar', validators=[Required()])
