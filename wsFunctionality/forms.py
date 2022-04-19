from wtforms import Form, StringField, validators

class DataInputForm(Form):
    name = StringField('Employee Name', [validators.Length(min=1, max=25)])
    sales = StringField('Sales amount in USD (rounded to nearest dollar)', [validators.Length(min=1, max=25)])