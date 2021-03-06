import datetime


class Response:
    """Represents a Response header.
       set_header_line must be set at the very least before being sent
    """
    def __init__(self):
        self.__header_fields = {}
        self.__version = ""
        self.__status = ""
        self.__status_value = 0
        self.__body = None

    def __getitem__(self, key):
        return self.__header_fields[key]

    def __setitem__(self, key, value):
        self.__header_fields[key] = value

    def __delitem__(self, key):
        del self.__header_fields[key]


    def set_header_line(self, version, value, status):
        self.__version = version
        self.__status = status
        self.__status_value = value

    def set_body(self, body):
        self.__body = body

    def generate(self):
        """Generates bytes object to be sent out to client (possibly with body)"""
        # Set the date time 
        current_time = datetime.datetime.now(tz=datetime.timezone.utc)

        # Check fields which can be autofilled
        if "Date" not in self.__header_fields:
            self["Date"] =  current_time.strftime("%a, %d %b %Y %H:%M:%S GMT")

        if self.__body is None:
            if "Content-Length" not in self.__header_fields:
                self["Content-Length"] =  str(0)
        else:
            self["Content-Length"] =  str(len(self.__body))

        if "Connection" not in self.__header_fields:
            self["Connection"] =  "closed"
      
        # render output
        out = self.__version + " " + str(self.__status_value) + " " + self.__status + "\r\n"
        for (k,v) in self.__header_fields.items():
            out += (k + ": " + v + "\r\n")
        out += "\r\n"
        if self.__body:
            return bytes(out, "utf-8") + self.__body
        else:
            return bytes(out, "utf-8")

def bad_request_400():
    header = Response()
    header.set_header_line("HTTP/1.1", 400, "Bad Request")
    return header


def ok_200():
    header = Response()
    header.set_header_line("HTTP/1.1", 200, "Ok")
    return header

def not_found_404():
    header = Response()
    header.set_header_line("HTTP/1.1", 404, "Not Found")
    return header

def method_not_allowed_405(allowed_methods):
    header = Response()
    header.set_header_line("HTTP/1.1", 405, "Method Not Allowed")
    allowed = ""
    for method in allowed_methods[:-1]:
        allowed += method + ', '
    allowed += allowed_methods[-1]
    header["Allow"] = allowed
    return header

