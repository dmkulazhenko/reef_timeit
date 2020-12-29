import os


def _get_absolute_endpoint(prefix: str, endpoint: str) -> str:
    return "{}/{}".format(prefix.rstrip("/"), endpoint.strip("/"))


class Config:
    # HUB Credentials
    HUB_APP_TOKEN = os.environ.get("HUB_APP_TOKEN")
    HUB_EMAIL = os.environ.get("HUB_EMAIL")
    HUB_PASSWORD = os.environ.get("HUB_PASSWORD")

    # Api Endpoints
    _API_URL = "https://api.hubstaff.com/v1/"

    # Auth
    API_END_AUTH = _get_absolute_endpoint(_API_URL, "/auth")

    # User
    API_END_USERS = _get_absolute_endpoint(_API_URL, "/users")
    API_END_USER = _get_absolute_endpoint(_API_URL, "/users/{}")

    # Project
    API_END_PROJECTS = _get_absolute_endpoint(_API_URL, "/projects")
    API_END_PROJECT = _get_absolute_endpoint(_API_URL, "/projects/{}")

    # Activity
    API_END_ACTIVITIES = _get_absolute_endpoint(_API_URL, "/activities")

    @classmethod
    def get_auth_data(cls):
        return {
            "headers": {"App-Token": cls.HUB_APP_TOKEN},
            "data": {"email": cls.HUB_EMAIL, "password": cls.HUB_PASSWORD},
        }
