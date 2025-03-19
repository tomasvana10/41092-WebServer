import os


def get_page_details(dir_: str = "pages") -> list[dict[str, str]]:
    details = []

    for filename in os.listdir(dir_):
        with open(os.path.join(dir_, filename), encoding="utf-8") as f:
            details.append({"filename": filename, "contents": f.read()})

    return details


def create_page(filename: str, contents: str, dir_: str = "pages") -> None:
    with open(os.path.join(dir_, filename), "x", encoding="utf-8") as f:
        f.write(contents)


def extract_req_filename(message: str) -> str:
    return message.split()[1][1:]


def extract_req_body(message: str) -> str:
    return "\r\n\r\n".join(message.split("\r\n\r\n")[1:])
