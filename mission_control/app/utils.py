import os
import json
import importlib
import inspect
import re


def fetch_config_path():
    flask_env_present = 'FLASK_ENV' in os.environ.keys()
    environment_present = 'ENVIRONMENT' in os.environ.keys()

    if environment_present and os.environ['ENVIRONMENT'] in VALID_FILENAMES:
        filename = VALID_FILENAMES[os.environ['ENVIRONMENT']]
    if flask_env_present and os.environ['FLASK_ENV'] in VALID_FILENAMES:
        filename = VALID_FILENAMES[os.environ['FLASK_ENV']]
    else:
        filename = VALID_FILENAMES['test']

    return os.path.abspath('./../{}'.format(filename))


VALID_FILENAMES = {
    'production': 'config.json',
    'development': 'config_development.json',
    'test': 'config_test.json'
}
CONFIG_PATH = fetch_config_path()
DEFAULT_INDENT = 2
IGNORABLES = ['csrf_token', 'submit']


class ConfigAlreadyExists(Exception):
    pass


class FormNotFound(Exception):
    pass


class FormSelector:
    @staticmethod
    def select_form_for_bot_type(bot_type):
        config = BotConfigBuilder.load_bot_config()
        titleized_handler = ''.join(x.title()
                                    for x in config['handler'].split('_'))
        form_class = 'Edit{}BotForm'.format(titleized_handler)

        if form_class in FormSelector.available_forms():
            module = importlib.import_module('app.forms')
            form = getattr(module, form_class)
            return form
        else:
            raise FormNotFound('Form "{}" not found.'.format(form_class))

    @staticmethod
    def available_forms():
        import app.forms as Forms

        return [class_[0] for class_ in inspect.getmembers(Forms, inspect.isclass) if FormSelector.is_valid_form(class_)]

    def is_valid_form(class_):
        return bool(re.match(r'Edit.*BotForm', class_[0]))


class BotConfigBuilder:
    @staticmethod
    def build_new(form_data, override=False):
        bot_config = BotConfigBuilder.load_bot_config()

        if bot_config != {} and not override:
            raise ConfigAlreadyExists(
                'Cannot overwrite existing bot configuration.')

        data = form_data.data.copy()
        BotConfigBuilder.ignore_useless_keys(data)
        bot_config = BotConfigBuilder.build_reddit_information(data)
        bot_config.update(data)

        BotConfigBuilder.save_bot_config(bot_config)

    @staticmethod
    def build_from_form(form_data):
        BotConfigBuilder.ignore_useless_keys(form_data, form=True)
        command_list = form_data['command_container']
        arranged_data = {command_list: []}

        for key in form_data:
            if key == 'command_container' or '_type' in key:
                continue

            function_name, new_key = key.split('-')

            function_already_present = False
            for datum in arranged_data[command_list]:
                if function_name in datum['function_name']:
                    if 'boolean' in new_key:
                        value = len(form_data[key]) > 0
                    else:
                        value = form_data[key]
                    datum[new_key] = BotConfigBuilder.coerce_data_to_correct_type(value, key, form_data)
                    function_already_present = True
                    continue

            if not function_already_present:
                arranged_data[command_list].append({
                    'function_name': function_name,
                    new_key: form_data[key]
                })

        config = BotConfigBuilder.load_bot_config()
        config.update(arranged_data)
        config[command_list] = [command for command in config[command_list]
                                if BotConfigBuilder.is_enabled(command)]
        BotConfigBuilder.save_bot_config(config)

    @staticmethod
    def config_already_exists():
        return os.path.exists(CONFIG_PATH) and BotConfigBuilder.load_bot_config() != {}

    @staticmethod
    def load_bot_config():
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as file:
                data = json.load(file)
        else:
            BotConfigBuilder.save_bot_config({})
            data = {}

        return data

    @staticmethod
    def save_bot_config(data):
        with open(CONFIG_PATH, 'w') as file:
            json.dump(data, file, indent=DEFAULT_INDENT)

    @staticmethod
    def delete_bot_config():
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)

    @staticmethod
    def build_reddit_information(data):
        REDDIT_FIELDS = ['username', 'password', 'client_id', 'client_secret']
        reddit_fields_dict = {}

        for field in REDDIT_FIELDS:
            reddit_fields_dict[field] = data.pop(field)

        with open(os.path.abspath('./../VERSION'), 'r') as file:
            version = file.read()

        reddit_fields_dict['user_agent'] = 'Reddit bot /u/{} powered by Gooey v{}'.format(
            reddit_fields_dict['username'], version)

        return {'reddit': reddit_fields_dict}

    @staticmethod
    def ignore_useless_keys(data, form=False):
        if form:
            ignorables = BotConfigBuilder.useless_form_fields(data)
        else:
            ignorables = IGNORABLES

        for ignorable in ignorables:
            data.pop(ignorable)

    @staticmethod
    def ignorable_view_fields():
        ignorables = ['command_container', 'submit', 'csrf_token']
        ignorables.append(IGNORABLES)

        return ignorables

    @staticmethod
    def useless_form_fields(data):
        return [field for field in data if field.split('-')[-1] in IGNORABLES]

    @staticmethod
    def is_enabled(command):
        return 'is_enabled_boolean' in command.keys() and command['is_enabled_boolean']

    @staticmethod
    def coerce_data_to_correct_type(value, function_name, fields):
        # Attempt to coerce data to the correct type given the form's hidden fields
        if 'is_enabled' in function_name:
            return value

        try:
            coercion_functions = {
                'string': str,
                'integer': coerce_to_int,
                'float': float
            }

            function_type_name = '{}_type'.format(function_name)
            function_type = fields[function_type_name]
            coercion_fn = coercion_functions[function_type]

            return coercion_fn(value)
        except Exception as e:
            return value


def titleize_snake_case(text, spaces=False):
    delimiter = ' ' if spaces else ''
    return delimiter.join([word.title() for word in text.split('_')])


def remove_boolean(text):
    return re.sub('Boolean', '', text)


def coerce_to_int(value):
    try:
        return int(float(value))
    except:
        return value
