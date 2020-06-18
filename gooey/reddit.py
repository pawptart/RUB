import praw


class Reddit:
    def __init__(self, config):
        self.config = config

    def build(self):
        reddit_config = self.config['reddit']

        return praw.Reddit(username=reddit_config['username'],
                           password=reddit_config['password'],
                           client_id=reddit_config['client_id'],
                           client_secret=reddit_config['client_secret'],
                           user_agent=reddit_config['user_agent'])
