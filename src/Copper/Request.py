class Request:
    def __init__(self):
        self.__method = None
        self.__path = None 
        self.__headers = {}

    def set_http_method(self, method):
        self.__method = method

    def get_http_method(self):
        return self.__method

    def get_header(self, key):
        return self.__headers[key]

    def set_path(self, path):
        self.__path = path

