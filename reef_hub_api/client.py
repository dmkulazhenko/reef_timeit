from datetime import datetime
from typing import Optional, Dict, Any, Union, List

import requests

from .auth import HubAuth
from .config import Config
from .exceptions import HubAuthCredentialsError, HubRequestError


class HubClient:
    def __init__(self):
        self.auth = HubAuth()

    def _request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Dict[Any, Any]] = None,
        _is_reauth: bool = False,
        **request_kwargs,
    ):
        def _add_auth_credentials(headers_: Dict[Any, Any]) -> Dict[Any, Any]:
            headers_ = headers_.copy()
            headers_.update(
                {
                    "App-Token": Config.HUB_APP_TOKEN,
                    "Auth-Token": self.auth.auth_token,
                }
            )
            return headers_

        if self.auth.auth_token is None or _is_reauth:
            self.auth.authenticate()

        headers = _add_auth_credentials({} if headers is None else headers)
        request = requests.request(
            method=method, url=url, headers=headers, **request_kwargs
        )

        if request.status_code == requests.codes.unauthorized:
            if not _is_reauth:
                return self._request(  # maybe token expired
                    method,
                    url,
                    headers=headers,
                    _is_reauth=True,
                    **request_kwargs,
                )
            # raise error if 401 even with new token
            raise HubAuthCredentialsError(request.json()["error"])
        elif request.status_code == requests.codes.not_found:
            return None

        result = request.json()
        if "error" in result:
            raise HubRequestError(result["error"])
        return result

    def _request_get(
        self, endpoint: str, params: Optional[Dict[Any, Any]] = None, **kwargs
    ) -> Optional[Union[List, Dict]]:
        return self._request("get", endpoint, params=params, **kwargs)

    def _request_post(
        self,
        endpoint: str,
        data: Optional[Dict[Any, Any]] = None,
        json: Optional[Dict[Any, Any]] = None,
        **kwargs,
    ) -> Optional[Union[List, Dict]]:
        return self._request("post", endpoint, data=data, json=json, **kwargs)

    def get_users(self, offset: int = 0) -> List[Dict[str, Any]]:
        request = self._request_get(
            Config.API_END_USERS, params={"offset": offset}
        )
        return request["users"]

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        request = self._request_get(Config.API_END_USER.format(user_id))
        return request["user"] if request is not None else request

    def get_projects(self, offset: int = 0) -> List[Dict[str, Any]]:
        request = self._request_get(
            Config.API_END_PROJECTS, params={"offset": offset}
        )
        return request["projects"]

    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        request = self._request_get(Config.API_END_PROJECT.format(project_id))
        return request["project"] if request is not None else request

    def get_activities(
        self, start_time: datetime, stop_time: datetime, offset: int = 0
    ) -> List[Dict[str, Any]]:
        params = {
            "start_time": start_time,
            "stop_time": stop_time,
            "offset": offset,
        }
        request = self._request_get(Config.API_END_ACTIVITIES, params=params)
        return request["activities"] if request is not None else request
