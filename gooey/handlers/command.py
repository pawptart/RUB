from handlers.errors import FunctionNotAllowed


class Command:
    def __init__(self, reddit, config):
        self.reddit = reddit
        self.config = config

        self.action_kwargs = self.config['action']['kwargs']

        fn_name = 'cmd_' + self.config['action']['name']
        self.fn = getattr(self, fn_name)

        if self.fn is None:
            raise FunctionNotAllowed(
                'Function "{}" not allowed'.format(fn_name))
