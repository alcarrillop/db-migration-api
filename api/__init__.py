from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

app.config.from_object('config.Config')  # Assuming you have a Config class in config.py
db = SQLAlchemy(app)

from api import routes, models


