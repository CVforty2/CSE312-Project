from io import BytesIO
from typing import *
from util.http.Response import Response
from util.debug.debug import debug_print
import re


class Requests:
    #path name must be regex. 
    #A function must also be passed to make a response, which accepts the actual path name
    
    def __init__(self, response_function: Callable[[Dict[str, Any], Dict[str, Any]], Response] = None, method: str = 'GET', path: str = "/") -> None:
        self.method: str = method
        self.path: str = path
        self.make_response = response_function
        self.path: re.Pattern[str] = re.compile(f"^\{path}$")
    
    #returns false if the request has not been handled.
    def handle_request(self, headers: Dict[str, Any], body: bytes, handler) -> bool:
        if self.method == headers.get('header info').get('method') and \
                self.path.match(headers.get('header info').get('path').get('route')):
            self.make_response(headers, body=(body.strip() if body else None)).send_response(handler)
            return True
            
        return False

#A buffered request is for a body largrer than 1024KB. It will get the remaineder of the bytes in a BytesIO object
#It will then read from that BytesIO, then pass the information to it's super class.
class BufferedRequest(Requests):
    def handle_request(self, headers: Dict[str, Any], body: bytes, handler) -> bool:
        if self.method == headers.get('header info').get('method') and \
                self.path.match(headers.get('header info').get('path').get('route')):
            stream: BytesIO = self.__finish_stream(headers, body, handler)
            return super().handle_request(headers, stream.read(), handler)
        return False
            
    def __finish_stream(self, headers: Dict[str, Any], body: bytes, handler) -> BytesIO:
        content_length: int = int(headers.get('Content-Length'))
        stream: BytesIO = BytesIO()
     
        #write the body to the stream
        if body:
            stream.write(body)
        
        debug_print("------------ Buffered Stream ------------")
        debug_print("------- BEFORE -------")
        debug_print(f"Actual Bytes Written: {stream.getbuffer().nbytes}\nTotal Bytes: {content_length}\nBytes Left To Write: {content_length - stream.getbuffer().nbytes}")
        debug_print("------- END -------")
        #keep reading from the handler until we get the total number of bytes
        while stream.getbuffer().nbytes < content_length:
            write_bytes: int = min(1024, content_length - stream.getbuffer().nbytes)
            stream.write(handler.request.recv(write_bytes))
        
        debug_print("------- AFTER -------")
        debug_print(f"Actual Bytes Written: {stream.getbuffer().nbytes}\nTotal Bytes: {content_length}\nBytes Left To Write: {content_length - stream.getbuffer().nbytes}")
        debug_print(f"Number of Bytes in the BytesIO Object: {stream.getbuffer().nbytes}")
        debug_print("------- END -------")
        debug_print("------------ END BUFFERED STREAM ------------")
        #reset the stream to the beginning
        stream.seek(0)
        return stream