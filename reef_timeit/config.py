import os
from datetime import timedelta
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).parent.absolute()

    # Fetchers
    # Represents the time period for which we will fetch data
    # must be less than 7 days
    FETCH_LAST_TIMEDELTA = timedelta(days=6, hours=23)
    # Represents the time period for which we will show default activity report
    DEFAULT_REPORT_TIMEDELTA = timedelta(days=1)

    # Logs
    LOG_DIR = Path(os.environ.get("LOG_DIR", BASE_DIR / "../logs"))
    LOG_FILE_NAME = "reef_timeit.log"

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / "reef_timeit.db")

    MYSQL_CREDENTIALS = (
        os.environ.get("MYSQL_CONNECTOR"),
        os.environ.get("MYSQL_USER"),
        os.environ.get("MYSQL_PASSWORD"),
        os.environ.get("MYSQL_HOST"),
        os.environ.get("MYSQL_DATABASE"),
    )
    if all(MYSQL_CREDENTIALS):
        SQLALCHEMY_DATABASE_URI = "mysql+{}://{}:{}@{}/{}".format(
            *MYSQL_CREDENTIALS
        )

    SQLALCHEMY_MIGRATIONS_DIR = (
        os.environ.get("SQLALCHEMY_MIGRATIONS_DIR") or "migrations"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Keys
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Crontab
    CRONTAB_LOCK_JOBS = True
