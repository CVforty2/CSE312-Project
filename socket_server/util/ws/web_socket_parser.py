import hashlib
import base64
from util.http import Response
from typing import *

WEB_SOCK_KEY: str = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

# returns an http 101 response
def web_socket_response(sec_socket_key: str) -> Response:
    print(f"sec_socket_key: {sec_socket_key}")
    print(f"WEB_SOCK_KEY: {WEB_SOCK_KEY}")
    sec_socket_accept: str = base64.b64encode(hashlib.sha1((sec_socket_key + WEB_SOCK_KEY).encode()).digest()).decode()
    return InitialSocketResponse(sec_socket_accept)

# overload the response class with a special websocket response
class InitialSocketResponse(Response.Response):
    def __init__(self, sec_socket_accept: str) -> None:
        super().__init__(status=101, message="Switching Protocols",\
             headerdict = {"Connection": "Upgrade", "Upgrade": "websocket", "Sec-WebSocket-Accept": sec_socket_accept},\
                  body = None)


