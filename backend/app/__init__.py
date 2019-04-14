from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__,template_folder='../templates')
app.config.from_object(Config)
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
