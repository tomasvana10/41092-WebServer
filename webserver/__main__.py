import socket as s 
import sys

from .server import init_server

with s.socket(s.AF_INET, s.SOCK_STREAM) as socket:
    port = int(sys.argv[1])
    socket.bind(("", port))
    socket.listen(1)

    print(f"Running server on port {port} (http://127.0.0.1:{port})")

    init_server(socket)
    socket.close()
    sys.exit()