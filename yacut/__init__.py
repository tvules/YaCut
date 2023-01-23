import sqlalchemy as sa
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import Model, SQLAlchemy

from settings import Config

app = Flask(__name__)
app.config.from_object(Config)


class IdModel(Model):
    """Base model."""

    id = sa.Column(sa.Integer, primary_key=True)


db = SQLAlchemy(app, model_class=IdModel)
migrate = Migrate(app, db=db)

from yacut import api_views, error_handlers, models, views
