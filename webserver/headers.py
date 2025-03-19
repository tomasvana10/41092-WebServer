STATUS_200 = "HTTP/1.1 200 OK"

STATUS_404 = "HTTP/1.1 404 Not Found"
BODY_404 = """
<!DOCTYPE html>
<html>
<head>
<title>Not found</title>
</head>
<body>
<h1>The requested page does not exist on the server.</h1>
</body>
</html>
"""

STATUS_500 = "HTTP/1.1 500 Internal Server Error"

CONTENT_TYPE = "Content-Type: {}"
CONTENT_LENGTH = "Content-Length: {}"
