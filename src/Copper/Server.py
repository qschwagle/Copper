import asyncio 
import datetime
import re
from Copper.Response    import Response, bad_request_400, ok_200
from Copper.Request     import Request
from Copper.FileManager import FileManager
from Copper.DummyService import DummyService


async def process_request(reader):
    """processes the request. Currently looks for the ending of the header
       the body of the request is not considered and none, part or whole maye
       be in the header
       can read infinitely or remain open infinitely (MEM/SOCK DOS Vulnerability)
       Note: Algorithm for searching HEADER termination is inefficient.
       Note: Request type and Content-Length must be read to read body
    """
    length = 1000
    matches = None 
    buffer = bytes("", "utf-8")
    req = Request()
    while not matches:
        read_data = await reader.read(length)
        if len(buffer) == 0:
            matcher = re.compile(bytes("(?P<method>(GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|TRACE)) (?P<resource>([*]|(/[0-9_a-zA-Z%]*)+)) (?P<http_version>(HTTP/1[.](0|1)))([\r][\n])", "utf-8"))
            req_type_match = matcher.match(read_data)
            if req_type_match:
                req.set_http_method(req_type_match.group('method'))
                req.resource = req_type_match.group('resource')
            else:
                return None
        buffer += read_data
        matches = re.search(bytes("[\r][\n][\r][\n]", "utf-8"), buffer)
    return req


class Server:
    def __init__(self):
        self._host = None
        self._port = None
        self._service = DummyService()

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, addr):
        self._host = addr

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, p):
        self._port = p

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, s):
        self._service = s


    def run(self):
        asyncio.run(self.server(self._host, self._port))

    async def server(self, host, port):
        srv = await asyncio.start_server(self.responder, host=host, port=port)
        await srv.serve_forever()

    async def responder(self, reader, writer):
        """
        server responder
        """
        request = await process_request(reader)
        if request is not None:
            res = await self._service.process(request)
            writer.write(res.generate())
            await writer.drain()
        else:
            res = bad_request_400()
            writer.write(res.generate())
            await writer.drain()
        writer.close()
