class Request:
    def __init__(self):
        self.__method = None
        self.__resource = None 
        self.__headers = {}

    def set_http_method(self, method):
        self.__method = method

    def get_http_method(self):
        return self.__method

    def __getitem__(self, key):
        return self.__headers[key]

    def __setitem__(self, key, value):
        self.__headers[key] = value

    def __delitem__(self, key):
        del self.__headers[key]


    def set_resource(self, resource):
        self.__resource = resource

