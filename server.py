import json
from pprint import pprint


import socket

from request import HttpRequest
from response import HttpResponse


def start_server() -> socket.socket:
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(('localhost', 8000))
    socket_server.listen(1)

    return socket_server

def log_request(data: bytes) -> None:
    print(data.decode())

def listen(server: socket.socket) -> None:
    while True:
        connection, address = server.accept()
        try:
            print("Connection received")
            data = connection.recv(4094)
            log_request(data)
            request = HttpRequest.parse_request(data)
            pprint(request.__dict__)
            
            response = HttpResponse(
                200, 
                {"MY_CUSTOM_HEADER": "MY_CUSTOM_HRADER_VALUE"}, 
                json.dumps({"some_body_value_name": "some_body_value"}).encode(),
            )

            log_request(response.encode())
            connection.sendto(response.encode(), address)
        except Exception as e:
            print("Failed to process request", e)
        finally:
            connection.close()


