from typing import Callable
from util.http import Routing
from util.ws import web_socket_parser, frame_parser
from util.debug.debug import debug_print
import base64
from util.ws.web_socket_connections import ws_connections
from typing import *

def add_routes(router: Routing.Routing):
    router.add_request(method='GET', path='/websocket', type='socket', response_generator=payload_handler)


def payload_handler(payload: bytes, **kwargs) -> None:
    debug_print('img recieved!')
    retVal = b'data:image/png;base64,' + base64.b64encode(payload)
    ws_connections.broadcast(frame_parser.WebSocketResponse(retVal).to_bytes())
    