from datetime import datetime
from enum import Enum
from typing import Tuple

from flask import request, current_app, flash


class FlashMessage(dict):
    class Color(str, Enum):
        RED = "danger"
        YELLOW = "warning"
        GREEN = "success"
        BLUE = "info"

    def __init__(self, color: Color, msg: str):
        self.color = color
        self.msg = msg
        super().__init__(color=color, msg=msg)


def parse_time_range() -> Tuple[datetime, datetime]:
    def get_default_time_range() -> Tuple[datetime, datetime]:
        stop_time_ = datetime.utcnow().replace(hour=0, minute=0, second=0)
        start_time_ = (
            stop_time_ - current_app.config["DEFAULT_REPORT_TIMEDELTA"]
        )
        return start_time_, stop_time_

    try:
        start_time = datetime.fromtimestamp(
            float(request.args.get("start_time"))
        )
        stop_time = datetime.fromtimestamp(
            float(request.args.get("stop_time"))
        )
        return start_time, stop_time
    except TypeError:
        return get_default_time_range()
    except Exception as exc:
        flash(
            FlashMessage(
                FlashMessage.Color.YELLOW,
                "From/To time is incorrect: {}".format(exc),
            ),
        )
        return get_default_time_range()
