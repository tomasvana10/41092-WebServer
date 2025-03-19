from typing import TypedDict


class BaseAPIResponseBody(TypedDict):
    status: str


class API200ResponseBody(BaseAPIResponseBody):
    pass


class API500ResponseBody(BaseAPIResponseBody):
    errName: str
    errMsg: str
