class Request:
    def __init__(self):
        self._method = None
        self._resource = None 
        self._headers = {}

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        self._method = method

    def __getitem__(self, key):
        return self._headers[key]

    def __setitem__(self, key, value):
        self._headers[key] = value

    def __delitem__(self, key):
        del self._headers[key]

    @property
    def resource(self):
        return self._resource
    
    @resource.setter
    def resource(self, resource):
        self._resource = resource

