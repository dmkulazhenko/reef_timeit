from logging import getLogger

from flask import render_template, send_file, flash, redirect, url_for
from sqlalchemy.exc import DatabaseError

from . import bp
from .utils import parse_time_range, FlashMessage
from .. import db
from ..fetchers import fetch_all
from ..models import Activity

logger = getLogger(__name__)


@bp.errorhandler(500)
def internal_error(err):
    db.session.rollback()
    logger.error("Caught 500: %s", err)
    return "Oh, internal server error"


@bp.route("/")
def index():
    start_time, stop_time = parse_time_range()

    activities = Activity.get_report(
        start_time=start_time,
        stop_time=stop_time,
    )
    return render_template(
        "main/index.html",
        activities=activities,
        start_time=(start_time, start_time.timestamp()),
        stop_time=(stop_time, stop_time.timestamp()),
    )


@bp.route("/csv_report")
def csv_report():
    start_time, stop_time = parse_time_range()
    return send_file(
        Activity.get_csv_report(start_time, stop_time),
        as_attachment=True,
        attachment_filename="timeit_report.csv",
        mimetype="text/csv",
    )


@bp.route("/update")
def update():
    try:
        fetch_all()
    except DatabaseError as exc:
        # cronjob can insert new data before us
        # and we will get duplicate -> exception
        flash(
            FlashMessage(
                FlashMessage.Color.RED,
                "Hmm... maybe cronjob or someone else already updated data?",
            )
        )
        logger.error("Error during update: %s", exc)
    else:
        flash(
            FlashMessage(FlashMessage.Color.GREEN, "Hooray! New data is here!")
        )
    return redirect(url_for("main.index"))
