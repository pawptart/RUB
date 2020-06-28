from reddit_mocks import *
from database.db import Database
from handlers.comment_stream import CommentStream
import unittest
import sys
import os
import pdb
import io
from contextlib import redirect_stdout


class TestCommentStream(unittest.TestCase):

    os.environ['ENVIRONMENT'] = 'test'
    BASE_CONFIG = {
        'action': {
            'kwargs': {}
        }
    }
    DB_PATH = Database().select_db_path()

    # Copied these from test_economy.py, not needed for now unless future features use the DB
    def setUp(self):
        if os.path.exists(self.DB_PATH):
            os.remove(self.DB_PATH)

    def tearDown(self):
        if os.path.exists(self.DB_PATH):
            os.remove(self.DB_PATH)

    def test_cmd_print(self):
        # Should print the comment to console
        cs_print_attributes = {
            **self.BASE_CONFIG,
            **{
                'comment_stream_commands': [
                    {
                        'name': 'print'
                    }
                ]
            }
        }
        comment_stream = CommentStream(MockReddit(), cs_print_attributes)
        comment = MockComment()

        # Decorator to redirect stdout
        f = io.StringIO()
        with redirect_stdout(f):
            comment_stream.cmd_print(comment)

        output = f.getvalue()

        self.assertIn(comment.body, output)

    def test_cmd_reply(self):
        # Should reply to each comment with a stock body
        cs_reply_attributes = {
            **self.BASE_CONFIG,
            **{
                'comment_stream_commands': [
                    {
                        'name': 'reply',
                        'contains': 'Reply!',
                        'case_sensitive': True,
                        'comment_reply_body': 'Reply body.'
                    }
                ]
            }
        }

        comment_stream = CommentStream(MockReddit(), cs_reply_attributes)
        valid_comment = MockComment(body='Reply!')
        invalid_comment = MockComment(body='Do not reply.')

        comment_stream.cmd_reply(valid_comment)
        self.assertEqual(len(valid_comment.replies), 1)
        self.assertEqual(valid_comment.replies[0].body, 'Reply body.')

        comment_stream.cmd_reply(invalid_comment)
        self.assertEqual(len(invalid_comment.replies), 0)

        cs_reply_case_sensitive_attributes = {
            **self.BASE_CONFIG,
            **{
                'comment_stream_commands': [
                    {
                        'name': 'reply',
                        'contains': 'reply!',
                        'case_sensitive': True,
                        'comment_reply_body': 'Reply body.'
                    }
                ]
            }
        }

        case_sensitive_stream = CommentStream(
            MockReddit(), cs_reply_case_sensitive_attributes)
        case_sensitive_stream.cmd_reply(valid_comment)
        # Should not change from 1
        self.assertEqual(len(valid_comment.replies), 1)

    def test_cmd_add_user_flair(self):
        pass
