from typing import *
from util.http.Response import Response
from util.static_info import static_variables

# This is a wrapper for a multiform. It function that accepts a function as 
# parameter that needs to take in headers and a body as a multiform. It returns a 
# function that parses the multiform and calls the parameter function
def multiform_function(response_function: Callable[[Dict[str, Any], Dict[str, Any]], Response])\
        -> Callable[[Dict[str, Any], Dict[str, Any]], Response]:
    def modified_response_function(headers, **kwargs) -> Response:
        body = kwargs.get('body')
        delimeter: bytes = ('--' + static_variables.boundary_gex.search(headers['Content-Type']).group(1)).encode()
        multi_form: List[Tuple[str, bytes]] = [__get_decoded_header(byte.split(b'\r\n\r\n'))\
            for byte in body.split(delimeter) if b'\r\n\r\n' in byte]
        return response_function(headers, multi_form=multi_form)

    return modified_response_function


def __get_decoded_header(input: List[bytes]) -> Tuple[str, bytes]:
    return (input[0].decode().strip('\r\n'), input[1].strip(b'\r\n'))