from sqlalchemy import func

from reef_timeit import db


class ModelBase(db.Model):
    __abstract__ = True

    @classmethod
    def get_max_hub_id(cls) -> int:
        # noinspection PyUnresolvedReferences
        return db.session.query(func.max(cls.hub_id)).scalar()

    def commit_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
