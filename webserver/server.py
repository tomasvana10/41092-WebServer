import json
import socket as s

from .enums import APIResponseStatus, APIRoute, RequestResult
from .headers import (
    BODY_404,
    CONTENT_LENGTH,
    CONTENT_TYPE,
    STATUS_200,
    STATUS_404,
    STATUS_500,
)
from .td import API200ResponseBody, API500ResponseBody
from .utils import create_page, extract_req_body, extract_req_filename, get_page_details


# Assumes the first element of headers is the status
def build_http_response(body: list[str] | str, *headers: str) -> bytes:
    req = ""
    req += "\r\n".join(headers) + "\r\n"

    # Add Content-Length header if it doesn't exist already.
    # This also makes the server HTTP/1.1 compatible
    if not any(header.startswith("Content-Length") for header in headers):
        if isinstance(body, list):
            req += f"{CONTENT_LENGTH.format(len('\r\n'.join(body).encode()))}\r\n"
        else:
            req += f"{CONTENT_LENGTH.format(len(body.encode()))}\r\n"

    req += "\r\n"

    if isinstance(body, list):
        for line in body:
            req += f"{line}\r\n"
    else:
        req += f"{body}\r\n"

    return req.encode()


def handle_request(
    conn: s.socket, addr: str
) -> RequestResult | tuple[RequestResult, str, str]:
    print(f"Connection from {addr}")

    try:
        message = conn.recv(1024).decode()
        if not message:
            return RequestResult.FAILURE

        filename = extract_req_filename(message)

        if not filename:  # User requested root directory ("/")
            filename = "pages/server.html"

        if filename.split("/")[-1] == "shutdown":
            return RequestResult.SHUTDOWN

        if filename.startswith("api/"):
            return (RequestResult.API_REQUEST, filename, message)

        with open(filename, encoding="utf-8") as f:
            lines = f.readlines()

        conn.send(build_http_response(lines, STATUS_200))
        return RequestResult.SUCCESS

    except IOError:
        conn.send(build_http_response(BODY_404, STATUS_404))
        return RequestResult.FAILURE


def handle_api_request(route: str, message: str) -> tuple[str, str] | tuple[str, ...]:
    dest = route.split("/")[-1]

    if dest == APIRoute.GET_PAGES.value:
        return (
            json.dumps(get_page_details()),
            STATUS_200,
            CONTENT_TYPE.format("application/json"),
        )

    if dest == APIRoute.POST_PAGE.value:
        try:
            body = json.loads(extract_req_body(message))
            create_page(body["filename"], body["contents"])
            return (
                json.dumps(
                    API200ResponseBody(status=APIResponseStatus.SUCCESS.value),
                ),
                STATUS_200,
            )
        except (json.JSONDecodeError, OSError) as err:
            return (
                json.dumps(
                    API500ResponseBody(
                        status=APIResponseStatus.FAILURE.value,
                        errName=type(err).__name__,
                        errMsg=str(err),
                    )
                ),
                STATUS_500,
            )

    else:
        return (
            json.dumps(
                API500ResponseBody(
                    status=APIResponseStatus.API_ENDPOINT_NOT_FOUND.value,
                    errName="",
                    errMsg="",
                )
            ),
            STATUS_404,
        )


def init_server(sock: s.socket) -> None:
    while True:
        conn, addr = sock.accept()
        request = handle_request(conn, addr)
        result = request if not isinstance(request, tuple) else request[0]

        match result:
            case RequestResult.SUCCESS:
                print(f"Successfully handled request of {addr}")
            case RequestResult.FAILURE:
                print(f"Failed to handle request of {addr}")
            case RequestResult.API_REQUEST:
                assert isinstance(request, tuple)
                args = handle_api_request(request[1], request[2])
                conn.send(build_http_response(*args))
                print(f"Handled API request of {addr}")
            case RequestResult.SHUTDOWN:
                conn.send(
                    build_http_response(json.dumps({"status": "success"}), STATUS_200)
                )
                print(f"{addr} requested to shut down server, shutting down...")
                break

        conn.close()
