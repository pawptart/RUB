import os
import sqlite3 as db


class Database:

    DB_PATH = {
        'production': './gooey.db',
        'development': './gooey_development.db',
        'test': './gooey_test.db'
    }

    def __init__(self):
        path = self.select_db_path()
        self.connection = db.connect(path)
        self.connection.row_factory = self.dict_factory

    def close(self):
        self.connection.close()

    def select_db_path(self):
        if os.environ['ENVIRONMENT'] in self.DB_PATH.keys():
            return self.DB_PATH[os.environ['ENVIRONMENT']]
        else:
            return self.DB_PATH['test']

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]

        return d
