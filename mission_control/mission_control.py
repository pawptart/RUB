from app import app
import os


@app.context_processor
def inject_dict_for_all_templates():
    return dict(VERSION=set_version())


def set_version():
    with open(os.path.abspath('./../VERSION'), 'r') as f:
        return f.read()
