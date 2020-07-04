from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

name_list = [(1, 'Error 1'), (2, 'Error 2'), (3, 'Error 3'), (4, 'Error 4'), (5, 'Error 5'), (0, 'No errors')]

class LinkForm(FlaskForm):
    link = SelectField(label='Error', choices=name_list, validators = [DataRequired()])
    submit = SubmitField('GO')

class GetSchemasForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    idDelete = StringField('idDelete', validators=[DataRequired()])
    newSchema = StringField('newSchema', validators=[DataRequired()])
    submit1 = SubmitField('Get certain scheme')
    submit2 = SubmitField('Get existing schemas')
    submit3 = SubmitField('Upload new schema')
    submit4 = SubmitField('Delete schema')

