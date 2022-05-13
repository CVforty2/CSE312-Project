import urllib.parse as parser
import html
from typing import *
from util.static_info import static_variables


#inputs: A header string (with \r\n)
#outputs: A dictionary representing the http headers
def get_headers(headers: str) -> Dict[str, Any]:
    httpheaders: Dict[str, Any] = {}
    headersaslist: List[str] = headers.split('\r\n')
    initialheaders = static_variables.httpheader.match(headersaslist[0])
    if initialheaders:
        httpheaders['header info'] = {
            'method': initialheaders.group(1),
            'path': __parse_path(initialheaders.group(2)),
            'http-version': initialheaders.group(3)
        }
    #get the rest of the headers
    for header_string in [headersaslist[i] for i in range(1, len(headersaslist))]:
        result = static_variables.keyvalue.match(header_string)
        if result:
            key, value = result.groups()
            httpheaders[key] = value
    
    return httpheaders

"""
route : 'some path',
queries: {
    key : value
} or None
"""
def __parse_path(path: str) -> Dict[str, Any]:
    path_query: List[str] = path.split('?')
    return {
        'route': path_query[0],
        'queries': __sanitize_dict(parser.parse_qs(path_query[1])) if len(path_query) > 1 else None
    }

#escapes all html
def __sanitize_dict(input: Dict[str, List[str]]) -> Dict[str, List[str]]:
    return {html.escape(key) : [html.escape(value) for value in sublist] for key, sublist in input.items()}