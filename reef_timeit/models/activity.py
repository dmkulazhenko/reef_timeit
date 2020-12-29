import csv
from datetime import datetime
from io import BytesIO, StringIO
from typing import List, Optional, Dict, Set, BinaryIO

from reef_timeit.models.project import Project
from reef_timeit.models.user import User
from .base import ModelBase
from .. import db


# noinspection PyUnresolvedReferences
class Activity(ModelBase):
    id = db.Column(db.Integer, primary_key=True)
    hub_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    stop_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    class Report:
        def __init__(
            self,
            users: Optional[List[User]] = None,
            stats: Optional[Dict[Project, Dict[User, int]]] = None,
        ):
            self.users: List[User] = users or []
            self.stats: Dict[Project, Dict[User, int]] = stats or {}

    @classmethod
    def get_by_time(
        cls, start_time: datetime, stop_time: datetime
    ) -> List["Activity"]:
        return cls.query.filter(
            cls.stop_time >= start_time,
            cls.start_time <= stop_time,
        ).all()

    @classmethod
    def get_report(cls, start_time: datetime, stop_time: datetime) -> Report:
        activities = cls.get_by_time(start_time, stop_time)

        report = cls.Report()
        users: Set[User] = set()

        for activity in activities:
            users.add(activity.user)

            if activity.project not in report.stats:
                report.stats[activity.project] = {}
            if activity.user not in report.stats[activity.project]:
                report.stats[activity.project][activity.user] = 0
            report.stats[activity.project][activity.user] += activity.duration

        report.users = list(users)

        return report

    # noinspection PyTypeChecker
    @classmethod
    def get_csv_report(
        cls, start_time: datetime, stop_time: datetime
    ) -> BinaryIO:
        report = cls.get_report(start_time, stop_time)
        csv_binary_stream = BytesIO()

        if len(report.users) > 0:
            csv_stream = StringIO()
            writer = csv.writer(csv_stream)
            writer.writerow(  # Add header like None, user1, user2, ...
                map(
                    lambda user: user.name if user is not None else None,
                    [None] + report.users,
                )
            )
            for project, project_stat in report.stats.items():
                writer.writerow(
                    [project.name]
                    + [project_stat.get(user, 0) for user in report.users]
                )

            # Creating the ByteIO object from the StringIO object
            csv_binary_stream.write(csv_stream.getvalue().encode("utf-8"))
            csv_binary_stream.seek(0)
            csv_stream.close()

        return csv_binary_stream
