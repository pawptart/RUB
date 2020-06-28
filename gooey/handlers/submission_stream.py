from handlers.errors import FunctionNotAllowed


class SubmissionStream:
    def __init__(self, reddit, config):
        self.reddit = reddit
        self.config = config

        self.action_kwargs = self.config['action']['kwargs']

        fn_name = 'cmd_' + self.config['action']['name']
        self.fn = getattr(self, fn_name)

        if self.fn is None:
            raise FunctionNotAllowed(
                'Function "{}" not allowed'.format(fn_name))

    def run(self):
        subreddit = self.config['subreddit']

        for submission in self.reddit.subreddit(subreddit).stream.submissions(**self.action_kwargs):
            self.fn(submission)

    def cmd_print(self, submission):
        if submission.is_self:
            print(submission.selftext)
        else:
            print(submission.url)

    def cmd_reply(self, submission):
        submission.reply(self.config['submission_reply_body'])

    def cmd_add_submission_flair(self, submission):
        if not self.config['submission_flair_condition']:
            return

        attributes = self.config['submission_flair_attributes']
        submission.mod.flair(attributes)

    def cmd_add_user_flair(self, submission):
        if not self.config['submission_author_flair_condition']:
            return

        redditor = submission.author
        attributes = self.config['submission_flair_attributes']
        redditor.mod.flair(attributes)

    def cmd_enforce_top_level_comment(self, submission):
        raise NotImplementedError
