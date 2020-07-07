from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length, AnyOf
from app.utils import titleize_snake_case
import os
import json

SCHEMA_PATH = os.path.abspath('./app/static/form_schema.json')


class BaseBotForm(FlaskForm):

    VALID_BOT_TYPES = ['economy', 'comment_stream']

    bot_pair_selection_options = [(bot_type, titleize_snake_case(bot_type, spaces=True))
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


class EditCommentStreamBotForm(FlaskForm):
    
    HANDLER_CONTAINER = 'comment_stream_commands'

    command_container = HiddenField(
        'command_container', default=HANDLER_CONTAINER)
    submit = SubmitField('Update')


class ActionFormLoader:

    FIELD_TYPES = {
        'string': StringField,
        'boolean': BooleanField,
        'integer': IntegerField,
        'float': FloatField
    }

    def __init__(self, form_class):
        self.form_class = form_class
        self.HANDLER_CONTAINER = form_class.HANDLER_CONTAINER

    def load_action_fields(self):
        # Load the JSON schema
        with open(SCHEMA_PATH) as file:
            json_file = json.load(file)
            schema = json_file[self.HANDLER_CONTAINER]

        # Iterate through the functions
        for function in schema:
            # Titleize the function name
            titleized_fn_name = titleize_snake_case(function['function_name'])
            # Build an ActionForm for the function
            function_subform_class = type('{}ActionForm'.format(
                titleized_fn_name), (FlaskForm, ), {})

            # Iterate through the values
            for field in function.keys():
                # Skip anything that doesn't have a valid field type
                value = function[field]
                if value not in self.FIELD_TYPES:
                    continue
                else:
                    field_name = titleize_snake_case(
                        field, spaces=True)
                    # Create an instance of the correct form given the built field name
                    field_instance = self.FIELD_TYPES[value](field_name)
                    # Set the function field to the ActionForm
                    setattr(function_subform_class, field, field_instance)
                    # Set the hidden field type for serializing data to JSON
                    hidden_field_name = '{}_type'.format(field)
                    hidden_field = HiddenField(hidden_field_name, default=value)
                    setattr(function_subform_class, hidden_field_name, hidden_field)

            # Set a BooleanField to enable the function
            setattr(function_subform_class, 'enabled',
                    BooleanField('Enabled'))
            # Set a type for the BooleanField
            enabled_hiddenfield = HiddenField('enabled_type', default='boolean')
            setattr(function_subform_class, 'enabled_type', enabled_hiddenfield)
            field_list = FormField(function_subform_class)
            # Set the entire field list to the initial form
            setattr(self.form_class, function['function_name'], field_list)
