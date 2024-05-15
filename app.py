from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()

# configuration
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres_flask_db:postgres@localhost:5432/postgres_db'  # environ.get('DB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# import routes
from .routes.auth_route import auth
from .routes.article_route import article

# register blueprint
app.register_blueprint(auth)
app.register_blueprint(article)

# initialize app
db.init_app(app)
