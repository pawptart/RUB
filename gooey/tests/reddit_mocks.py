import uuid
import weakref


class MockReddit:
    def __init__(self):
        self.user = MockUser()


class MockComment:
    def __init__(self, comment_id=None, author=None, body='test', parent=None, replies=None):
        self.id = comment_id if comment_id else str(uuid.uuid1())
        self.author = author if author else MockUser()
        self.body = body
        self.parent = parent
        self.replies = [] if replies == None else replies
        self.last_reply = self.last_reply_body()

    def reply(self, text):
        comment = MockComment(body=text, parent=self)
        self.replies.append(comment)
        self.last_reply = self.last_reply_body()
        return comment

    def last_reply_body(self):
        if len(self.replies) > 0:
            return self.replies[-1].body
        else:
            return []


class MockUser:
    def __init__(self, user_id=None, name='RedditGooeyBot'):
        self.id = user_id if user_id else str(uuid.uuid1())
        self.name = name

    def me(self):
        return self
