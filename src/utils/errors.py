class BaseError(Exception):
    pass


class HttpxClientError(BaseError):
    pass


class ClickhouseError(BaseError):
    pass
