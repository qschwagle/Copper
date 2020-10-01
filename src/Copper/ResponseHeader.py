import datetime


class ResponseHeader:
    """Represents a Response header.
       set_header_line must be set at the very least before being sent
    """
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
        """Generates bytes object to be sent out to client (possibly with body)"""
        # Set the date time 
        current_time = datetime.datetime.now(tz=datetime.timezone.utc)

        # Check fields which can be autofilled
        if "Date" not in self.__header_fields:
            self.set_field("Date", current_time.strftime("%a, %d %b %Y %H:%M:%S GMT"))

        if "Content-Length" not in self.__header_fields:
            self.set_field("Content-Length", str(0))

        if "Connection" not in self.__header_fields:
            self.set_field("Connection", "closed")
      
        # render output
        out = self.__version + " " + str(self.__status_value) + " " + self.__status + "\r\n"
        for (k,v) in self.__header_fields.items():
            out += (k + ": " + v + "\r\n")
        out += "\r\n"
        return bytes(out, "utf-8")


def bad_request_400():
    header = ResponseHeader()
    header.set_header_line("HTTP/1.1", 400, "Bad Request")
    return header


def ok_200():
    header = ResponseHeader()
    header.set_header_line("HTTP/1.1", 200, "OK")
    return header

