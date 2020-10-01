import asyncio 
import datetime


class Header:
    def __init__(self):
        self.__header_fields = {}
        self.__version = ""
        self.__status = ""
        self.__status_value = 0

    def set_field(self, key, value):
        self.__header_fields[key] = value

    def get_field(self, key):
        return self.__header_fields[key]

    def set_header_line(self, version, value, status):
        self.__version = version
        self.__status = status
        self.__status_value = value

    def generate(self):
        out = self.__version + " " + str(self.__status_value) + " " + self.__status + "\r\n"
        for (k,v) in self.__header_fields.items():
            out += (k + ": " + v + "\r\n")
        out += "\r\n"
        return bytes(out, "utf-8")


async def responder(reader, writer):
    header = Header()
    header.set_header_line("HTTP/1.1", 200, "OK")
    header.set_field("Connection", "closed")
    header.set_field("Content-Type", "text/html; charset=utf-8")
    current_time = datetime.datetime.now(tz=datetime.timezone.utc)
    header.set_field("Date", current_time.strftime("%a, %d %b %Y %H:%M:%S GMT"))
    body = bytes("<html><body><h1>hello world</h1></body></html>","utf-8")
    header.set_field("Content-Length", str(len(body)))
    header_out =  header.generate()
    writer.write(header_out + body)
    await writer.drain()
    writer.close()

async def server():
    srv = await asyncio.start_server(responder, host="0.0.0.0", port="8080")
    await srv.serve_forever()


async def main():
    print("Hello, World")
    await server()


asyncio.run(main())
