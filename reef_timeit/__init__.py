import logging
from logging.handlers import RotatingFileHandler
from typing import Type

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_crontab import Crontab
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from reef_hub_api import HubClient
from reef_timeit.config import Config

bootstrap = Bootstrap()
crontab = Crontab()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

hub_client = HubClient()


def create_app(config_class: Type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Connect plugins to Flask
    bootstrap.init_app(app)
    crontab.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    # Register blueprints
    from .main import bp as main_bp

    app.register_blueprint(main_bp)

    # Register cron jobs
    from .crontab_jobs import fetcher_job

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

    return app
