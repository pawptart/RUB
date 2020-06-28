from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length, AnyOf
from app.utils import titleize_snake_case, remove_boolean
import os
import json

SCHEMA_PATH = os.path.abspath('./app/static/form_schema.json')


class ActionForm(FlaskForm):
    pass


class BaseBotForm(FlaskForm):

    VALID_BOT_TYPES = ['economy']

    bot_pair_selection_options = [(bot_type, bot_type.title())
                                  for bot_type in VALID_BOT_TYPES]
    bot_pair_selection_options.insert(0, (None, 'Select Type'))

    username = StringField('Reddit Username', validators=[DataRequired()])
    password = PasswordField('Reddit Password', validators=[DataRequired()])
    client_id = PasswordField('Client ID', validators=[DataRequired()])
    client_secret = PasswordField('Client Secret', validators=[DataRequired()])
    handler = SelectField('Bot Type', choices=bot_pair_selection_options, default=0, validators=[
                          DataRequired(), AnyOf(values=VALID_BOT_TYPES)])
    submit = SubmitField('Create')


class EditEconomyBotForm(FlaskForm):

    HANDLER_CONTAINER = 'economy_commands'

    command_container = HiddenField(
        'command_container', default=HANDLER_CONTAINER)
    submit = SubmitField('Update')


class ActionFormLoader:

    FIELD_TYPES = {
        'string': StringField,
        'boolean': BooleanField,
        'integer': IntegerField
    }

    def __init__(self, form_class):
        self.form_class = form_class
        self.HANDLER_CONTAINER = form_class.HANDLER_CONTAINER

    def load_action_fields(self):
        with open(SCHEMA_PATH) as file:
            json_file = json.load(file)
            schema = json_file[self.HANDLER_CONTAINER]

        for function in schema:
            titleized_fn_name = titleize_snake_case(function['function_name'])
            function_subform_class = type('{}ActionForm'.format(
                titleized_fn_name), (FlaskForm, ), {})

            for field in function.keys():
                value = function[field]
                if value not in self.FIELD_TYPES:
                    continue
                else:
                    titleized_field_name = titleize_snake_case(
                        field, spaces=True)
                    field_name = remove_boolean(titleized_field_name)
                    field_instance = self.FIELD_TYPES[value](field_name)
                    setattr(function_subform_class, field, field_instance)

            setattr(function_subform_class, 'is_enabled_boolean',
                    BooleanField('Enabled'))
            field_list = FormField(function_subform_class)
            setattr(self.form_class, function['function_name'], field_list)
