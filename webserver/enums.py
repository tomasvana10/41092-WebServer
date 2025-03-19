from enum import IntEnum, StrEnum


class RequestResult(IntEnum):
    SUCCESS = 0
    FAILURE = 1
    SHUTDOWN = 2
    API_REQUEST = 3


class APIRoute(StrEnum):
    GET_PAGES = "getPages"
    POST_PAGE = "postPage"


class APIResponseStatus(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    API_ENDPOINT_NOT_FOUND = "api-endpoint-not-found"
