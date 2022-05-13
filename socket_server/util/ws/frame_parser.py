from io import BytesIO
from typing import *
from util.http import Requests, Response
from util.ws import web_socket_parser
from util.ws.util import parse_bytes
from util.ws.web_socket_connections import ws_connections
from util.debug import debug
import re

# A class holding the frames for the web socket
class WebSocketFrame():
    def __init__(self, opcode: int, payload_len: int, masking_key: bytes, payload_complete: bool) -> None:
        self.fin = 0
        self.opcode: int = opcode
        self.payload_len: int = payload_len
        self.masking_key: bytes = masking_key
        self.payload_complete: bool = payload_complete

    def __repr__(self) -> str:
        return f'WebSocketFrame<fin={self.fin}, opcode={self.opcode}, payload_len={self.payload_len},\
            masking_key={self.masking_key}, payload_complete={self.payload_complete}>'

def parse_frame(frame: bytes) -> Tuple[WebSocketFrame, bytes]:
    retFrame: WebSocketFrame = WebSocketFrame(0, 0, None, False)
    # Get the fin bit
    retFrame.fin = frame[0] >> 7
    # first 8 bits are the op code
    retFrame.opcode = parse_bytes._OPCODE(frame[0 : 1])
    # get the payload
    temp_payload: int = parse_bytes._PAYLOAD(frame[1 : 2])
    # when the masking key begins
    masking_key_offset: int = 2
    # case 1: payload len is 126, read bytes 2 and 3 to get payload len
    if temp_payload == 126: 
        temp_payload = parse_bytes._EXTPAYLOAD(frame[2 : 4])
        masking_key_offset = 4
    # case 1: payload len is 126, read bytes 2 through 9 to get payload len
    elif temp_payload == 127:
        temp_payload = parse_bytes._EXTEXTPAYLOAD(frame[2 : 10])
        masking_key_offset = 10
    retFrame.payload_len = temp_payload
    # requested 1024 bytes and adjust at most 14 bytes for the headers, if the payload length is within 1010 bytes, we do not need to finish the request
    retFrame.payload_complete = retFrame.payload_len <= 1010
    # next 4 bytes is the masking key
    retFrame.masking_key = frame[masking_key_offset: masking_key_offset + 4]
    # everything afterward is the body
    return (retFrame, frame[masking_key_offset + 4: ])



# A web socket request. In handle_requests, goes through an infinite loop until the client closes the connection, where it returns true.
class WebSocketRequest(Requests.BufferedRequest):
    def __init__(self, web_socket_function, method: str = 'GET', path: str = "/") -> None:
        # a function that accepts a payload of bytes and does something with it
        self.web_socket_function = web_socket_function
        self.method: str = method
        self.path: re.Pattern[str] = re.compile(f"^\{path}$")
    
    def handle_request(self, headers: Dict[str, Any], body: bytes, handler) -> bool:
        if self.method == headers.get('header info').get('method') and \
                self.path.match(headers.get('header info').get('path').get('route')):
            # send the response, but don't return anything!
            web_socket_parser.web_socket_response(headers.get('Sec-WebSocket-Key')).send_response(handler)
            # add the handler to the set of ws connections
            ws_connections.add_connection(handler)
            debug.debug_print(ws_connections.ws_connections)
            # enter the infinite loop
            while True:
                try:
                    # request initially 1kb
                    # parse the frame and finish the stream. The stream should contain the entire body decoded.
                    frame, payload = parse_frame(handler.request.recv(1024))
                    if frame.opcode == 8: break # 1000 means close the connection.

                    # If the fin bit is 1, that means this is the last frame. Else, we keep grabbing frames until the fin bit is 1.
                    # Ran into issues where a large image would be broken into smaller frames!
                    if frame.fin == 1:
                        if not frame.payload_complete: 
                            stream: BytesIO = self.__finish_stream(frame, payload, handler)
                            # call the callback function with the entire payload. It should return a frame response
                            self.web_socket_function(payload=self.__decode(stream.read(), frame.masking_key).strip(), handler=handler)
                        else:
                            self.web_socket_function(payload=self.__decode(payload, frame.masking_key).strip(), handler=handler)
                    
                    else:
                        global_payload = self.__decode(payload if frame.payload_complete\
                             else self.__finish_stream(frame, payload, handler).read(), frame.masking_key)
                        
                        while frame.fin != 1:
                            debug.debug_print("still getting...")
                            frame, payload = parse_frame(handler.request.recv(1024))
                            global_payload += self.__decode(payload if frame.payload_complete\
                                else self.__finish_stream(frame, payload, handler).read(), frame.masking_key)
                        
                        self.web_socket_function(payload=global_payload.strip(), handler=handler)

                except Exception as error:
                    debug.debug_print(str(error))
                    break
            # remove the handler from the set of ws connections
            ws_connections.remove_connection(handler)
            debug.debug_print(ws_connections.ws_connections)
            return True
        else:
            return False

    #finish reading the body as neccessary and xor the bytes before writing to the stream.
    def __finish_stream(self, frame: WebSocketFrame, payload: bytes, handler) -> BytesIO:
        content_length: int = frame.payload_len
        stream: BytesIO = BytesIO()
     
        #write the body to the stream
        stream.write(payload)
        
        #keep reading from the handler until we get the total number of bytes
        while stream.getbuffer().nbytes < content_length:
            write_bytes: int = min(1024, content_length - stream.getbuffer().nbytes)
            stream.write(handler.request.recv(write_bytes))
    
        #reset the stream to the beginning
        stream.seek(0)
        return stream
    
    # decode the payload. The payload must be complete
    def __decode(self, payload: bytes, masking_key: bytes) -> bytes:
        decoded_payload: bytes = bytes()
        for i in range(0, len(payload), 4):
            decoded_payload += self.__xor_payload(payload[i: i + 4], masking_key[0: min(4, len(payload) - i)])
        return decoded_payload

    def __xor_payload(self, payload_chunk: bytes, masking_key: bytes) -> bytes:
        return (int.from_bytes(payload_chunk, 'big') ^ int.from_bytes(masking_key, 'big')).to_bytes(len(payload_chunk), 'big')


class WebSocketResponse(Response.Response):
    def __init__(self, payload: bytes) -> None:
        self.payload: bytes = payload
    
    def __get_response(self) -> bytes:
        if self.payload:
            op_code: bytes = (129).to_bytes(1, 'big') # get OP code
            payload_len: bytes = None
            # greater than 65536
            if len(self.payload) >= (1 << 16): payload_len = (127).to_bytes(1, 'big') + len(self.payload).to_bytes(8, 'big')
            # greater than 126
            elif len(self.payload) >= ((1 << 7) - 2): payload_len = (126).to_bytes(1, 'big') + len(self.payload).to_bytes(2, 'big')
            # less than 126
            else: payload_len = len(self.payload).to_bytes(1, 'big')
            # return the bytes
            return op_code + payload_len + self.payload
        else:
            op_code: bytes = (136).to_bytes(1, 'big') # get OP code
            payload_len: bytes = (0).to_bytes(1, 'big')
            return op_code + payload_len
    
    def to_bytes(self):
        return self.__get_response()

    def send_response(self, handler):
        #handler.request.sendall(self.__get_response())
        pass
