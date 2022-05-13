# Module handles the web socket connections and storing the state of them.
# Because of the multithreading nature of this, we need to implent locks.

from threading import Lock
from socketserver import BaseRequestHandler
from typing import *

ws_lock: Lock = Lock()
ws_connections: Set[BaseRequestHandler] = set()

def add_connection(handler: BaseRequestHandler):
    ws_lock.acquire()
    ws_connections.add(handler)
    ws_lock.release()

def remove_connection(handler: BaseRequestHandler):
    ws_lock.acquire()
    ws_connections.remove(handler)
    ws_lock.release()

def broadcast(payload: bytes):
    ws_lock.acquire()
    for handler in ws_connections: handler.request.sendall(payload)
    ws_lock.release()

# Like broadcast, except for everything except the parameter handler.
def broadcast_except(handler: BaseRequestHandler, payload: bytes):
    ws_lock.acquire()
    for handler_send in ws_connections: 
        if handler_send is not handler: handler_send.request.sendall(payload)
    ws_lock.release()