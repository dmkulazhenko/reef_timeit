from .base import ModelBase
from .. import db


class Project(ModelBase):
    id = db.Column(db.Integer, primary_key=True)
    hub_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    name = db.Column(db.String(length=512), nullable=False)
    activities = db.relationship("Activity", backref="project", lazy="dynamic")
