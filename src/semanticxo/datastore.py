'''
Created on 24 Sep 2011

@author: cgueret
'''
from rdflib import ConjunctiveGraph, RDF, URIRef, Namespace, Literal
from semanticxo.sparql import SPARQL
import httplib
import time
import logging

OLPC = Namespace("http://example.org/")
OLPC_TERMS = Namespace("http://example.org/terms#")

_QUERY_INT_KEY = ['timestamp', 'filesize', 'creation_time']

class TripleStore(object):
    '''
    The TripleStore is a generic object interface with a triple store
    '''
    def __init__(self, params = None):
        '''
        Constructor of the TripleStore
        if an hostname is indicated, query the triple store of that machine
        instead of the one at localhost
        '''
        hostname = 'localhost'
        if params != None:
            if 'hostname' in params.keys():
                hostname = params['hostname']
        self.store_url = '%s:8080' % hostname
        print self.store_url
        self.device_uid = 'ABC1234567890' #TODO find how to get the serial number

    def _get_resource(self, uid):
        '''
        Return the URI associated to a particular UID
        '''
        return URIRef(OLPC['resource/%s' % uid])

    def get_object(self, uid, properties=None):
        '''
        Get a specific object associated to this UID
        '''
        metadata = {}
        query = 'SELECT ?p ?o WHERE { <%s> ?p ?o. }' % self._get_resource(uid)
        sparql = SPARQL()
        for result in sparql.execute_select(query):
            if result['p'].startswith(OLPC_TERMS):
                key=result['p'].split(OLPC_TERMS)[1]
                if key in _QUERY_INT_KEY:
                    metadata[key] = int(result['o'])
                else:
                    metadata[key] = result['o']
                    
        # HACK: This is expected to be always present
        if 'creation_time' not in metadata:
            metadata['creation_time'] = int(time.time())

        return metadata
    
    def store_object(self, uid, metadata):
        '''
        Store an object defined by a uid and its associated metadata
        '''
        metadata['uid'] = uid
        
        # Preprocess the metadata
        props = {}
        for key, value in metadata.items():

            # Hack to support activities that still pass properties named as
            # for example title:text.
            if ':' in key:
                key = key.split(':', 1)[0]

            # Re-encode strings
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif not isinstance(value, basestring):
                value = str(value)
            
            # Save new binding
            props[key] = value

        # Compose and save the graph
        graph = ConjunctiveGraph()
        resource = self._get_resource(uid)
        graph.add((resource, RDF.type, OLPC_TERMS['DSObject']))
        for key, value in props.items():
            if isinstance(key, basestring) and isinstance(value, basestring):
                key = OLPC_TERMS[key]
                try:
                    value = Literal(value)
                    graph.add((resource, key, value))
                except:
                    pass
                
        # Save it
        logging.debug('[MDS] save > %s' % graph.serialize())
        headers = { 'Accept' : '*/*', 'Content-Type': 'application/rdf+xml' }
        conn = httplib.HTTPConnection(self.store_url)
        conn.request("PUT", "/data/%s" % resource, body=graph.serialize(), headers=headers)
        conn.getresponse()
        conn.close()
        
        