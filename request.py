import json
from typing import Self


def _parse_params(raw: bytes) -> dict[str, str]:
    params: dict[str, str] = {}
    for param in raw.split(b"&"):
        name = param.split(b"=")[0].decode()
        value = param.split(b"=")[1].decode()
        params[name] = value
    
    return params

def _parse_headers(raw: list[bytes]) -> dict[str, str]:
        headers: dict[str, str] = {}
        # Parse headers
        for line in raw:
            name = line.split(b":", 1)[0].decode()
            value = line.split(b":", 1)[1][:-1].decode()
            headers[name] = value
        
        return headers

class HttpRequest:
    method: str
    route: str
    params: dict[str, str]
    headers: dict[str, str]
    body: bytes
    
    def json(self) -> dict:
        return json.loads(self.body)


    @staticmethod
    def parse_request(data: bytes) -> "HttpRequest":
        request = HttpRequest()

        # Parse request metadata
        data_lines = data.split(b"\n")
        metadata = data_lines[0].split(b" ")
        request.method = metadata[0].decode()
        url =  metadata[1]
        request.route = url.split(b"?")[0].decode()
        request.params = _parse_params(url.split(b"?")[1])

        request.headers = _parse_headers(data_lines[1:-2])

        # Read body
        request.body = data_lines[-1]

        return request
        