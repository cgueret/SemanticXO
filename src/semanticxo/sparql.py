'''
Created on 25 Aug 2011

@author: cgueret
'''
import httplib
import urllib
import cjson
from rdflib import URIRef, Literal

class SPARQL(object):
    '''
    classdocs
    '''


    def __init__(self, url):
        '''
        Constructor
        '''
        self._url = url
        
    def execute_select(self, query):
        params = {'query': query, 'format' : 'json'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        conn = httplib.HTTPConnection(self._url)
        conn.request("POST", "/sparql", urllib.urlencode(params), headers=headers)
        # Get the results
        response = conn.getresponse()
        r = cjson.decode(response.read(), all_unicode=False)
        # Recode them
        results = []
        for entry in r['results']['bindings']:
            result = {}
            for (name,data) in entry.iteritems():
                value = Literal(data['value'])
                if data['type']=='uri':
                    value = URIRef(data['value'])
                result[name] = value
            results.append(result)
        conn.close()
        return results
