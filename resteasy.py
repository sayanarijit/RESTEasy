# -*-coding: utf-8 -*-

"""
Author          : Arijit Basu <sayanarijit@gmail.com>
Website         : https://sayanarijit.github.io
"""

from __future__ import absolute_import, unicode_literals
import json
import requests
from copy import deepcopy


class RESTEasy(object):
    """REST API client session creator.

    Arguments:
        base_url (str): Base URL of the API service.

    Optional keyword arguments:
        encoder (callable): Encoder used to encode data to be posted.
        decoder (callable): Decoder used to decode returned data.
        timeout (float): Default request timeout.
        debug (bool): Toggle debug mode.
        kwargs (dict): Extra arguments to update `requests.Session` object.
    """

    def __init__(
            self, base_url, encoder=json.dumps, decoder=json.loads,
            timeout=None, debug=False, **kwargs):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers['Content-Type'] = 'application/json'
        self.session.headers['Accept'] = 'application/json'
        self.session.__dict__.update(kwargs)
        self.timeout = timeout
        self.encoder = encoder
        self.decoder = decoder
        self.debug = debug

    def route(self, *args):
        """Return endpoint object.

        Arguments:
            args (list): Route URL path.

        Returns:
            APIEndpoint: Object that supports CRUD queries.
        """

        return APIEndpoint(
            endpoint='{}/{}'.format(
                self.base_url, ('/'.join(map(str, args)))),
            session=deepcopy(self.session), timeout=self.timeout,
            encoder=self.encoder, decoder=self.decoder, debug=self.debug)


class APIEndpoint(object):
    """API endpoint supports CRUD queries.

    Arguments:
        endpoint (str): Full URL of the API endpoint.
        session (requests.Session): A copy of `requests.Session` object.

    Optional keyword arguments:
        encoder (callable): Encoder used to encode data to be posted.
        decoder (callable): Decoder used to decode returned data.
        timeout (float): Default request timeout.
        debug (bool): Toggle debug mode.
    """

    def __init__(self, endpoint, session, encoder=json.dumps,
                 decoder=json.loads, timeout=None, debug=False):
        self.endpoint = endpoint
        self.session = session
        self.timeout = timeout
        self.encoder = encoder
        self.decoder = decoder
        self.debug = debug

    def route(self, *args):
        """Routes to a new endpoint.

        Arguments:
            args (list): Route URL path.

        Returns:
            APIEndpoint: Object that supports CRUD queries.
        """

        return APIEndpoint(
            endpoint='{}/{}'.format(
                self.endpoint, ('/'.join(map(str, args)))),
            session=deepcopy(self.session), timeout=self.timeout,
            encoder=self.encoder, decoder=self.decoder, debug=self.debug)

    def request(self, method, **kwargs):
        """A shortcut to the `self.session.request` method.

        Arguments:
            method (str): HTTP request method.
            kwargs (dict): Arguments to pass to the `self.session.request` method.

        Returns:
            requests.Response|dict: Raw response object or dictionary in case of debug.
        """
        if self.debug:
            return dict(kwargs, endpoint=self.endpoint, method=method)
        return self.session.request(method, self.endpoint, **kwargs)

    def do(self, method, kwargs={}):
        """Do the HTTP request.

        Arguments:
            method (str): HTTP request method.
            kwargs (dict): Request parameters in case of GET/DELETE, else request data.

        Returns:
            self.decoder(str): Decoded response object.
        """

        if method == 'GET' or method == 'DELETE':
            response = self.request(method, params=kwargs, timeout=self.timeout)
        else:
            response = self.request(
                method, data=self.encoder(kwargs), timeout=self.timeout)

        if self.debug:
            return response

        response.raise_for_status()

        content = response.content.decode('latin1')
        return self.decoder(content)

    def get(self, **kwargs): return self.do('GET', kwargs)
    def post(self, **kwargs): return self.do('POST', kwargs)
    def put(self, **kwargs): return self.do('PUT', kwargs)
    def patch(self, **kwargs): return self.do('PATCH', kwargs)
    def delete(self, **kwargs): return self.do('DELETE', kwargs)
