from Copper.Request import Request
from Copper.Response import Response, ok_200, not_found_404, method_not_allowed_405

class DummyService:
    """Service mountable to Server"""
    def __init__(self):
        pass

    async def process(self, req: Request) -> Response:
        print(req.resource)
        if req.resource == b'/get' and req.method != b'GET':
            res = method_not_allowed_405(['GET'])
            return res
        elif req.resource == b'/':
            res = ok_200()
            res["Content-Type"] = "text/html; charset=utf-8"
            res.set_body(bytes("<html><body><h1>hello world</h1></body></html>","utf-8"))
            return res
        else:
            res = not_found_404()
            res["Content-Type"] = "text/html; charset=utf-8"
            res.set_body(bytes("<html><body><h1>Not Found</h1></body></html>","utf-8"))
            return res
