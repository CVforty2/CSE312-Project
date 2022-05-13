from typing import *


class Response:
    def __init__(self, status: int = 200, message: str = "OK", \
        headerdict: Dict[str, str] = {}, body: bytes = None) -> None:
        self.status: int = status
        self.message: str = message
        self.header_info: Dict[str, str] = headerdict
        self.body: bytes = body

    #returns an HTTP response as a bytes object
    def __get_response(self) -> bytes:
        if len(self.header_info) > 0:
            if self.body:
                return (f"HTTP/1.1 {self.status} {self.message}\r\n" + \
                        "".join(f"{key}:{value}\r\n" for key, value in self.header_info.items()) + \
                            "X-Content-Type-Options: nosniff\r\n" + \
                                f"Content-Length:{len(self.body)}\r\n\r\n").encode() + self.body
            else:
                return (f"HTTP/1.1 {self.status} {self.message}\r\n" + \
                          "".join(f"{key}:{value}\r\n" for key, value in self.header_info.items()) + \
                            "X-Content-Type-Options: nosniff\r\n" + \
                                f"Content-Length:{0}\r\n\r\n").encode()
        else:
            return (f"HTTP/1.1 {self.status} {self.message}\r\n" + \
                        "X-Content-Type-Options: nosniff\r\n" + \
                            f"Content-Length:{0}\r\n\r\n").encode()
    
    def send_response(self, handler):
        handler.request.sendall(self.__get_response())

    def to_bytes(self):
        return self.__get_response()


HTTP404: Response = Response(
    status = 404,
    message="Not Found",
    headerdict={
        "Content-Type": "text/plain"
    }, body="The requested content does not exist".encode()
)

HTTP403: Response = Response(
    status=403,
    message="Forbidden",
    headerdict={
        "Content-Type": "text/plain"
    }, body="You do not have permission to view the requested content".encode()
)

class HTTP301(Response):
    def __init__(self, location: str) -> None:
        super().__init__(
            status=301,
            message="Moved Permanently",
            headerdict={
                "Location": location
            }
        )

class HTTP400(Response):
    def __init__(self, user_message: str) -> None:
        super().__init__(
            status=400,
            message="Invalid Request",
            headerdict={
                "Content-Type": "text/plain"
            }, body=user_message.encode()
        )