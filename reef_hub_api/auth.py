from logging import getLogger
from typing import Optional

import requests

from .config import Config
from .exceptions import HubAuthCredentialsError, HubAuthError

logger = getLogger(__name__)


class HubAuth:
    def __init__(self):
        self.auth_token: Optional[str] = None

    def authenticate(self) -> str:
        logger.info("Obtaining a new auth token")
        request = requests.post(
            Config.API_END_AUTH,
            timeout=Config.REQUEST_TIMEOUT,
            **Config.get_auth_data(),
        )

        if request.status_code == requests.codes.ok:
            self.auth_token = request.json()["user"]["auth_token"]
        elif request.status_code == requests.codes.unauthorized:
            raise HubAuthCredentialsError(request.json()["error"])
        else:
            raise HubAuthError(request.json()["error"])

        return self.auth_token
