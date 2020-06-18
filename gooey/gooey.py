import importlib
import json
from handlers.errors import HandlerNotAllowed
from handlers.config import *
from reddit import Reddit
import sys
import traceback
import os

_VALID_FILENAMES = {
    'production': 'config.json',
    'development': 'config_development.json',
    'test': 'config_test.json'
}
_ENVIRONMENT = os.environ['FLASK_ENV'] if 'FLASK_ENV' in os.environ.keys(
) else 'development'
os.environ['ENVIRONMENT'] = _ENVIRONMENT
_CONFIG_FILENAME = _VALID_FILENAMES[_ENVIRONMENT]
_CONFIG_PATH = os.path.abspath('./{}'.format(_CONFIG_FILENAME))


class Gooey:

    config = load_config(_CONFIG_PATH)
    _ALLOWED_HANDLERS = load_allowed_handlers('./gooey/handlers')

    def __init__(self):
        self.handler = self.select_handler()

    def select_handler(self):
        handler = 'handlers.{}'.format(self.config['handler'])
        if self.config['handler'] in self._ALLOWED_HANDLERS:
            class_ = ''.join(x.title()
                             for x in self.config['handler'].split('_'))
            module = importlib.import_module(handler)
            handler_class = getattr(module, class_)
            return handler_class(Reddit(config).build(), self.config)
        else:
            raise HandlerNotAllowed('Handler "{}" not allowed'.format(handler))

    def start(self):
        self.handler.run()


if __name__ == '__main__':
    config = load_config(_CONFIG_PATH)
    if 'run_in_loop' in config.keys() and config['run_in_loop'] == True:
        while True:
            try:
                Gooey().start()
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception:
                traceback.print_exc()
    else:
        Gooey().start()
