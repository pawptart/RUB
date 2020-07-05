from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)

from app import routes
