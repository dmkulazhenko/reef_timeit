from . import crontab
from .fetchers import fetch_all


@crontab.job(minute="*/15")
def fetcher_job():
    fetch_all()
