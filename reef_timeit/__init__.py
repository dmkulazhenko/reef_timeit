import logging
from logging.handlers import RotatingFileHandler
from typing import Type

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from reef_timeit.config import Config

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class: Type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Connect plugins to Flask
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    # Setup logging
    app.config["LOG_DIR"].mkdir(exist_ok=True)
    file_handler = RotatingFileHandler(
        str(app.config["LOG_DIR"] / app.config["LOG_FILE_NAME"]),
        maxBytes=2097152,
        backupCount=10,
    )

    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s "
            "[in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("TimeIt Startup")

    return app
