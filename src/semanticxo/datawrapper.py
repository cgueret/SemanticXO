'''
Created on Oct 8, 2011

@author: cgueret
'''
import surf
import urllib2
import cjson
from semanticxo.datastore import TripleStore

class DataWrapper(object):
    '''
    The Data wrapper is a class that is used to have a direct 
    access (i.e. without dbus) to the journal on the XOs. It 
    also serves as an interface with public data stores such 
    as DBpedia
    '''
    def __init__(self, store):
        '''
        Create an instance of the wrapper connected to 
        a specific end point
        '''
        try:
            # Get the SPARQL end point from CKAN
            endpoint = None
            data = cjson.decode(urllib2.urlopen('http://thedatahub.org/api/rest/package/%s' % store).read())
            for resource in data['resources']:
                if resource['format'] == 'api/sparql':
                    endpoint = resource['url']
                    
            # Initialize the store
            self._store = surf.Store(reader='sparql_protocol', endpoint=endpoint)
        except:
            # Initialize a local store
            self._store = TripleStore(hostname=store)
            
    def get_instances(self, uri_class):
        session = surf.Session(self._store, {})
        session.enable_logging = False
        instances = session.get_class(uri_class).all()
        return instances
    
    def get_datastore_instances(self):
        instances = []
        for uid in self._store.get_uids():
            instance = self._store.get_object(uid)
            instances.append(instance)
        return instances
    
    def get_datastore_instance(self, uid):
        return self._store.get_object(uid)
    
if __name__ == '__main__':
    wrapper = DataWrapper(store='dbpedia')
    print surf.ns.YAGO['CitiesInTheNetherlands']
    cities = wrapper.get_instances(surf.ns.YAGO['CitiesInTheNetherlands'])
    for city in cities:
        print city.foaf_name
