import json
import os

DISALLOWED_HANDLERS = ['errors', 'config']


def load_config(filename):
    path = build_absolute_path('../../{}'.format(filename))
    with open(path) as f:
        data = json.load(f)

    return data


def load_allowed_handlers():
    handlers_path = build_absolute_path('.')
    files = os.listdir(handlers_path)

    return [format_handler(handler) for handler in files if valid_handler(handler)]


def format_handler(handler):
    return handler.split('.py')[0]


def valid_handler(handler):
    for invalid_handler in DISALLOWED_HANDLERS:
        if invalid_handler in handler:
            return False

    return '.py' in handler


def build_absolute_path(relative_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    combined_relative_path = os.path.join(current_dir, relative_path)

    return os.path.abspath(combined_relative_path)
