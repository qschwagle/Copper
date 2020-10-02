from Copper.Request import Request
from Copper.Response import Response, ok_200

class DummyService:
    """Service mountable to Server"""
    def __init__(self):
        pass

    async def process(self, req: Request) -> Response:
        res = ok_200()
        res["Content-Type"] = "text/html; charset=utf-8"
        res.set_body(bytes("<html><body><h1>hello world</h1></body></html>","utf-8"))
        return res
