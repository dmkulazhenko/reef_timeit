from datetime import datetime
from logging import getLogger
from typing import Iterable, Any

from flask import current_app

from reef_timeit import hub_client, db
from reef_timeit.models import User, Project, Activity
from .casters import json_to_user, json_to_project, json_to_activity

logger = getLogger(__name__)


def bulk_save(items: Iterable[Any]) -> None:
    try:
        db.session.bulk_save_objects(items)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        raise exc


# ------------------------ IMPORTANT ------------------------ #
# This methods have non-obvious execution order,              #
# You must execute fetch of users/projects before activities. #
# As far as if user/project doesn't exist                     #
# -> you cannot associate activity with user/project.         #
# ------------------------ IMPORTANT ------------------------ #


def _fetch_users() -> None:
    max_hub_id = User.get_max_hub_id()
    users = hub_client.get_users(
        offset=(max_hub_id + 1 if max_hub_id is not None else 0)
    )
    bulk_save(map(json_to_user, users))


def _fetch_projects() -> None:
    max_hub_id = Project.get_max_hub_id()
    projects = hub_client.get_projects(
        offset=(max_hub_id + 1 if max_hub_id is not None else 0)
    )
    bulk_save(map(json_to_project, projects))


def _fetch_activities() -> None:
    max_hub_id = Activity.get_max_hub_id()
    activities = hub_client.get_activities(
        start_time=(
            datetime.utcnow() - current_app.config["FETCH_LAST_TIMEDELTA"]
        ),
        stop_time=datetime.utcnow(),
        offset=(max_hub_id + 1 if max_hub_id is not None else 0),
    )
    bulk_save(map(json_to_activity, activities))


def fetch_all() -> None:
    logger.info("Fetching process start")
    _fetch_users()
    _fetch_projects()
    _fetch_activities()
    logger.info("Fetching process end")
