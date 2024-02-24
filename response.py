_CODE_REASONS = {
    200: "OK",
    400: "Bad Request",
    404: "Not Found"
}

_LINE_BREAK = b"\r\n"

class HttpResponse:
    protocol: str
    status_code: int
    headers: dict[str, str]
    body: bytes

    def __init__(
        self,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        body: bytes | None = None,
    ) -> None:
        self.protocol = "HTTP/1.1"
        self.status_code = status_code
        self.headers = headers or {}
        self.body = body or bytes()

    def encode(self) -> bytes:
        response: list[bytes] = []

        response += [
            self.protocol.encode(), b" ", 
            str(self.status_code).encode(), b" ", 
            _CODE_REASONS[self.status_code].encode(), _LINE_BREAK
        ]

        self.headers["Content-Length"] = str(len(self.body))
        self.headers["Server"] = "my custom server/0.0.1"
        self.headers["Connection"] = "Closed"
        self.headers["Content-Type"] = "application/json"
        for k, v in self.headers.items():
            response += [k.encode(), b": ", v.encode(), _LINE_BREAK]
        
        response += [_LINE_BREAK, self.body]

        return b"".join(response)
