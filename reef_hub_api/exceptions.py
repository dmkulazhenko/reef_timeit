class HubError(Exception):
    pass


# Auth

class HubAuthError(HubError):
    pass


class HubAuthCredentialsError(HubError):
    pass


# Global API

class HubRequestError(HubError):
    pass
