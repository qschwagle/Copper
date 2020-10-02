from Copper.Request import Request
from Copper.Response import Response, ok_200, method_not_allowed_405

class FileManager:
    """Service mountable to Server"""
    def __init__(self):
        self._serving_directory = "."
        self._show_listing = False

    @property
    def show_listing(self):
        return self._show_listing

    @show_listing.setter
    def show_listing(self, p):
        self._show_listing = p

    @property
    def serving_directory(self):
        return self._serving_directory

    @serving_directory.setter
    def serving_directory(self, sd):
        """future: recursively checks for permissions for this directory and below"""
        self._serving_directory = sd

    async def get_file(self, path):
        """get file from path"""
        pass

    async def get_listing(self, path):
        """retrieves a listing"""
        pass

    async def process(self, req: Request) -> Response:
        if req.method != b'GET':
            res = method_not_allowed_405(['GET'])
            return res
        else:
            res = ok_200()
            res["Content-Type"] = "text/html; charset=utf-8"
            res.set_body(bytes("<html><body><h1>hello world</h1></body></html>","utf-8"))
            return res
