import asyncio 
import datetime
import re
from ResponseHeader import ResponseHeader


class HttpRequest:
    def __init__(self):
        self.__method = None

    def set_http_method(self, method):
        self.__method = method

    def get_http_method(self):
        return self.__method


async def process_request(reader):
    """processes the request. Currently looks for the ending of the header
       the body of the request is not considered and none, part or whole maye
       be in the header
       can read infinitely or remain open infinitely (MEM/SOCK DOS Vulnerability)
       Note: Algorithm for searching HEADER termination is inefficient.
       Note: Request type and Content-Length must be read to read body
    """
    finished_reading = False
    length = 1000
    matches = None 
    buffer = bytes("", "utf-8")
    req = HttpRequest()
    while not matches:
        read_data = await reader.read(length)
        if len(buffer) == 0:
            matcher = re.compile(bytes("(GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|TRACE)", "utf-8"))
            req_type_match = matcher.match(read_data)
            if req_type_match:
                req.set_http_method(req_type_match.group(0))
            else:
                return None

        buffer += read_data
        matches = re.search(bytes("[\r][\n][\r][\n]", "utf-8"), buffer)
    return req


class HttpResponse:
    def __init__(self):
        pass


async def responder(reader, writer):
    request = await process_request(reader)
    if request is not None:
        header = ResponseHeader()
        header.ok_request()
        header.set_field("Content-Type", "text/html; charset=utf-8")
        body = bytes("<html><body><h1>hello world</h1></body></html>","utf-8")
        header.set_field("Content-Length", str(len(body)))
        header_out =  header.generate()
        writer.write(header_out + body)
        await writer.drain()
    else:
        header = ResponseHeader()
        header.bad_request()
        header_out =  header.generate()
        writer.write(header_out)
        await writer.drain()
    writer.close()


async def server():
    srv = await asyncio.start_server(responder, host="0.0.0.0", port="8080")
    await srv.serve_forever()
