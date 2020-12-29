from datetime import timedelta
from typing import Dict, Any

from .utils import iso8601_to_datetime
from reef_timeit.models import User, Project, Activity


def json_to_user(json_user: Dict[str, Any]) -> User:
    return User(
        hub_id=json_user["id"],
        name=json_user["name"],
        email=json_user["email"],
    )


def json_to_project(json_project: Dict[str, Any]) -> Project:
    return Project(
        hub_id=json_project["id"],
        name=json_project["name"],
    )


# noinspection PyUnresolvedReferences
def json_to_activity(json_activity: Dict[str, Any]) -> Activity:
    user = User.query.filter_by(hub_id=json_activity["user_id"]).first()
    project = Project.query.filter_by(
        hub_id=json_activity["project_id"]
    ).first()

    start_time = iso8601_to_datetime(json_activity["starts_at"])
    stop_time = start_time + timedelta(seconds=json_activity["tracked"])

    return Activity(
        hub_id=json_activity["id"],
        start_time=start_time,
        stop_time=stop_time,
        duration=json_activity["tracked"],
        user_id=user.id if user is not None else None,
        project_id=project.id if project is not None else None,
    )
