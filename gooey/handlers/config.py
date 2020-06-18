import json
import os

DISALLOWED_HANDLERS = ['errors', 'config']


def load_config(path):
    with open(path) as f:
        data = json.load(f)

    return data


def load_allowed_handlers(path):
    files = os.listdir('./gooey/handlers')

    return [format_handler(handler) for handler in files if valid_handler(handler)]


def format_handler(handler):
    return handler.split('.py')[0]


def valid_handler(handler):
    for invalid_handler in DISALLOWED_HANDLERS:
        if invalid_handler in handler:
            return False

    return '.py' in handler
