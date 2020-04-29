# -*-coding: utf-8 -*-

"""
Author          : Arijit Basu <sayanarijit@gmail.com>
Website         : https://sayanarijit.github.io
"""

from __future__ import absolute_import, unicode_literals
import json
import requests
from copy import deepcopy

GET = "GET"
POST = "POST"
PUT = "PUT"
HEAD = "HEAD"
PATCH = "PATCH"
DELETE = "DELETE"


class RESTEasy(object):
    """REST API client session creator.

    Arguments:
        endpoint (str): Base URL of the API service.

    Optional keyword arguments:
        encoder (callable): Encoder used to encode data to be posted.
        decoder (callable): Decoder used to decode returned data.
        timeout (float): Default request timeout.
        allow_redirects (bool): Set to True by default.
        debug (bool): Toggle debug mode.
        session (request.Session): Use the given session instead of creating a new one.
        kwargs (dict): Extra arguments to update `requests.Session` object.
    """

    GET = GET
    POST = POST
    PUT = PUT
    PATCH = PATCH
    HEAD = HEAD
    DELETE = DELETE

    def __init__(
        self,
        endpoint,
        encoder=None,
        decoder=None,
        timeout=None,
        allow_redirects=True,
        debug=False,
        session=None,
        **kwargs
    ):
        self.endpoint = endpoint
        if session is None:
            self.session = requests.Session()
            self.session.headers["Content-Type"] = "application/json"
            self.session.headers["Accept"] = "application/json"
        else:
            self.session = session
        self.session.__dict__.update(kwargs)
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.encoder = json.dumps if encoder is None else encoder
        self.decoder = json.loads if decoder is None else decoder
        self.debug = debug

    def route(self, *args):
        """Routes to a new endpoint.

        Arguments:
            args (list): Route URL path.

        Returns:
            RESTEasy: Object that supports CRUD queries.
        """

        return type(self)(
            endpoint="{}/{}".format(self.endpoint, "/".join(map(str, args))),
            timeout=self.timeout,
            encoder=self.encoder,
            decoder=self.decoder,
            debug=self.debug,
            session=deepcopy(self.session),
        )

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

    def do(self, method, kwargs=None):
        """Do the HTTP request.

        Arguments:
            method (str): HTTP request method.
            kwargs (dict): Request parameters in case of GET/DELETE, else request data.

        Returns:
            self.decoder(str): Decoded response object.
        """
        if kwargs is None:
            kwargs = {}

        if method == self.GET or method == self.DELETE:
            response = self.request(
                method,
                params=kwargs,
                timeout=self.timeout,
                allow_redirects=self.allow_redirects,
            )
        else:
            response = self.request(
                method,
                data=self.encoder(kwargs),
                timeout=self.timeout,
                allow_redirects=self.allow_redirects,
            )

        if not self.debug and self.allow_redirects and "Location" in response.headers:
            api = deepcopy(self)
            api.endpoint = response.headers["Location"]
            response = api.request(api.GET)

        if self.debug:
            return response

        response.raise_for_status()

        content = response.content.decode("latin1")
        return self.decoder(content)

    def get(self, **kwargs):
        return self.do(self.GET, kwargs)

    def post(self, **kwargs):
        return self.do(self.POST, kwargs)

    def put(self, **kwargs):
        return self.do(self.PUT, kwargs)

    def patch(self, **kwargs):
        return self.do(self.PATCH, kwargs)

    def delete(self, **kwargs):
        return self.do(self.DELETE, kwargs)
