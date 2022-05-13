from typing import *
from util.debug.debug import debug_print
from util.http.Requests import Requests, BufferedRequest
from util.ws.frame_parser import WebSocketRequest
from util.http.Response import Response, HTTP404

#handles routing
class Routing:
    def __init__(self) -> None:
        self.routes: List[Requests] = []
        self.http_404: Response = HTTP404
    
    #adds a request
    def add_request(self, method: str, path: str, response_generator, type: str = "") -> None:
        if type == "Buffered":
            self.routes.append(BufferedRequest(response_function=response_generator, method=method, path=path))
        elif type == "socket":
            self.routes.append(WebSocketRequest(web_socket_function=response_generator, method=method, path=path))
        else:
            self.routes.append(Requests(response_function=response_generator, method=method, path=path))

    #goes through all of the routes and attempts to satisfy the request
    def handle_routes(self, handler, headers: Dict[str, Any], body: bytes):
        for request in self.routes:
            try:
                if request.handle_request(headers, body, handler):
                    return
            except AttributeError as error:
                debug_print("Error found, but if expected, carry on... " + str(error))
                break
                      
        self.http_404.send_response(handler)