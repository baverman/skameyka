from taburetkit import ObjectDecoder

try:
    import simplejson as json
except ImportError:
    import json


class Form(object):
    pass


class TreeViewControl(object):
    def render(self):
        pass


class TreeViewEndpointDataSource(object):
    def get_nodes(self, root=None):
        params = {'root':root} if root else None
        return json.loads(self.client.invoke(self.endpoint, params=params))    


def make_object_decoder(client):
    classmap = {
        'Form': Form,
        'TreeViewControl': TreeViewControl,
        'TreeViewEndpointDataSource': TreeViewEndpointDataSource,
    }
    
    injectmap = {
        'TreeViewEndpointDataSource': {
            'client': client
        }
    }
    
    return ObjectDecoder(classmap, injectmap)