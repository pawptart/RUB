from handlers.errors import FunctionNotAllowed


class CommentStream:
    def __init__(self, reddit, config):
        self.reddit = reddit
        self.config = config
        self.action_kwargs = self.config['action']['kwargs']

        # TODO: Consider refactoring to work more like Economy class (support multiple commands)
        self.fn_attributes = self.config['comment_stream_commands'][0]
        self.fn = getattr(self, 'cmd_' + self.fn_attributes['name'])

        if self.fn is None:
            raise FunctionNotAllowed(
                'Function "{}" not allowed'.format(fn_name))

    def run(self):
        subreddit = self.config['subreddit']

        for comment in self.reddit.subreddit(subreddit).stream.comments(**self.action_kwargs):
            self.fn(comment)

    def cmd_print(self, comment):
        print(comment.body)

    def cmd_reply(self, comment):
        trigger = self.fn_attributes['contains']
        body = comment.body

        if not self.fn_attributes['case_sensitive']:
            trigger = trigger.lower()
            body = body.lower()

        if trigger not in body:
            return

        reply_body = self.fn_attributes['comment_reply_body']
        comment.reply(reply_body)

    def cmd_add_user_flair(self, comment):
        redditor = comment.author
        attributes = self.config['comment_flair_attributes']
        redditor.mod.flair(attributes)

    # TODO: The below functions are currently not used, should be refactored as above
    def cmd_find_command(self, comment):
        for command in self.config['comment_commands']:
            if command['case_insensitive'] == True:
                command_text = command['text'].lower()
                comment_body = comment_body.lower()
            else:
                command_text = command['text']
                comment_body = comment_body

            if command_text in comment_body:
                self.cmd_call_command_function(comment, command)

    def cmd_call_command_function(self, comment):
        raise NotImplementedError
