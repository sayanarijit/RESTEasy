# -*-coding: utf-8 -*-

"""
Author          : Arijit Basu <sayanarijit@gmail.com>
Website         : https://sayanarijit.github.io
"""

from __future__ import absolute_import, unicode_literals
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class HTTPError(Exception):
    def __init__(self, status, content):
        Exception.__init__(self, 'Server returned HTTP status code: {}\n{}'.format(status, content))

class InvalidResponseError(Exception):
    def __init__(self, content):
        Exception.__init__(self, 'Server returned JSON incompatible response:\n{}'.format(content))


class RESTEasy(object):
    """
    REST session creator
    """
    def __init__(self, base_url, auth=None, verify=False, cert=None, timeout=None,
                 encoder=json.dumps, decoder=json.loads):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = auth
        self.session.verify = verify
        self.session.cert = cert
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.timeout = timeout
        self.encoder = encoder
        self.decoder = decoder

    def route(self, *args):
        """
        Return endpoint object
        """
        return APIEndpoint(
            endpoint=self.base_url + '/' + ('/'.join(map(str, args))),
            session=self.session, timeout=self.timeout,
            encoder=self.encoder, decoder=self.decoder
        )


class APIEndpoint(object):
    """
    API endpoint
    """
    def __init__(self, endpoint, session, timeout=None, encoder=json.dumps, decoder=json.loads):
        self.endpoint = endpoint
        self.session = session
        self.timeout = timeout
        self.encoder = json.dumps
        self.decoder = json.loads

    def route(self, *args):
        """
        Return endpoint object
        """
        return APIEndpoint(
            endpoint=self.endpoint + '/' + ('/'.join(map(str, args))),
            session=self.session, timeout=self.timeout,
            encoder=self.encoder, decoder=self.decoder
        )

    def do(self, method, **kwargs):
        """
        Do the HTTP request
        """
        method = method.upper()
        if method == 'GET':
            response = self.session.get(self.endpoint,
                    params=kwargs, timeout=self.timeout)
        else:
            response = self.session.request(method, self.endpoint,
                    data=self.encoder(kwargs), timeout=self.timeout)

        if response.status_code not in range(200,300):
            raise HTTPError(response.status_code, response.content)

        try:
            return self.decoder(response.content)
        except Exception:
            raise InvalidResponseError(response.content)

    def get(self, **kwargs): return self.do('GET', **kwargs)
    def post(self, **kwargs): return self.do('POST', **kwargs)
    def put(self, **kwargs): return self.do('PUT', **kwargs)
    def patch(self, **kwargs): return self.do('PATCH', **kwargs)
    def delete(self, **kwargs): return self.do('DELETE', **kwargs)
