from typing import Any


class RESTSdkException(Exception):
    pass


class WrongRtypeException(RESTSdkException):
    pass


class WrongDataException(RESTSdkException):
    pass

class WrongJsonException(RESTSdkException):
    pass

class WrongDataBaseException(RESTSdkException):
    pass