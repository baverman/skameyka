import urlparse
import httplib
import urllib

class Client(object):
    def __init__(self, endpoint):
        self.connection = None
        
        url = urlparse.urlsplit(endpoint)
        
        self.hostname = url.hostname
        self.connection_class = {
            'http': httplib.HTTPConnection,
            'https': httplib.HTTPSConnection
        }[url.scheme]
        
        self.port = url.port
        self.prefix = url.path
        
        if self.prefix.endswith('/'):
            self.prefix = self.prefix[:-1]
        
    def get_connection(self):
        if not self.connection:
            self.connection = self.connection_class(self.hostname, self.port)
            
        return self.connection 
    
    def __del__(self):
        self.close()
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def invoke(self, path, params=None, body=None):
        method = 'POST' if body else 'GET'
        query = ('?' + urllib.urlencode(params)) if params else ''
        
        if path.startswith('http://') or path.startswith('https://'):
            path = urlparse.urlsplit(path).path + query
        else:
            path = self.prefix + path + query
        
        headers = {
            'Connection': 'keep-alive',
        }
        
        conn = self.get_connection()
        conn.request(method, path, body, headers)
        return conn.getresponse().read()
    
    def index(self):
        return self.invoke('/')
    

class ObjectDecoder(object):
    def __init__(self, classmap, injectmap):
        self.classmap = classmap
        self.injectmap = injectmap
        
    def decode(self, data):
        return self.__decode_object(None, data)
    
    def __decode_object(self, object, data):
        if object is None:
            if isinstance(data, dict):
                if '_type' in data:
                    type_name = data['_type']
                    object = self.classmap[type_name]()
                    if type_name in self.injectmap:
                        for k, v in self.injectmap[type_name].items():
                            setattr(object, k, v)
                    return self.__decode_object(object, data)
                else:
                    return data
            elif isinstance(data, list):
                return self.__decode_object([], data)
        else:
            if isinstance(data, dict):
                for k, v in data.items():
                    if k != '_type':
                        setattr(object, k, self.__decode_object(None, v))
                return object
            elif isinstance(data, list):
                for v in data:
                    object.append(self.__decode_object(None, v))
                return object
            
        return data