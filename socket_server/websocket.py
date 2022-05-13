import socketserver
from util.http.Routing import Routing
from util.ws.web_socket_route import add_routes as ws_routes
from util.http.http_parser import header_parser
from util.debug.debug import debug_print
from typing import *
from sys import argv

#delcare all variables
routes: Routing = Routing()
ws_routes(routes)

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).split(b'\r\n\r\n', 1)
        decoded_data: Tuple[str, bytes] = (self.data[0].decode(), self.data[1] if len(self.data) > 1 else None)      
        parsed_http: Dict[str, Any] = header_parser.get_headers(decoded_data[0])
        #debug_print(parsed_http)
        routes.handle_routes(self, parsed_http, decoded_data[1])
            

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", int(argv[1]) if len(argv) > 1 else 8000


    # Create the server, binding to localhost on port 9999
    with socketserver.ThreadingTCPServer((HOST, PORT), TCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        debug_print(f"Serving on address {HOST} and port {PORT}")
        server.serve_forever()