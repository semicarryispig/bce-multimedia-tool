"""
This module provides media auth
"""
import datetime
import bcesigner
import logging
try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse
import uuid

from requests.auth import AuthBase


class MediaAuth(AuthBase):
    """
    media auth extends authBase
    """
    service_base_url = 'localhost'

    def __init__(self, access_key, secret_key, service_url=None):
        if service_url:
            self.service_base_url = service_url
        self.access_key = str(access_key)
        self.secret_key = str(secret_key)

    def __call__(self, r):
        """
        :param r:
        :return:
        """
        parsedurl = urlparse(r.url)
        uri = parsedurl.path
        request = self.get_request(r.method, uri, parsedurl.query)
        request = self.generate_signature(request)
        r.headers['x-bce-date'] = request['headers']['x-bce-date']
        r.headers['x-bce-request-id'] = request['headers']['x-bce-request-id']
        r.headers['host'] = request['headers']['host']
        r.headers['content-type'] = request['headers']['content-type']
        r.headers['authorization'] = request['headers']['authorization']
        r.params = request['params']
        r.method = request['method']
        r.uri = request['uri']
        return r

    def generate_signature(self, request):
        """
        :param request:
        :return:
        """
        signer = bcesigner.BceSigner(self.access_key, self.secret_key)
        signer.logger.setLevel(logging.WARNING)
        auth = signer.gen_authorization(request, timestamp=request['headers']['x-bce-date'])

        request['headers']['authorization'] = auth
        request['headers']['x-bce-request-id'] = str(uuid.uuid4())
        request['headers']['content-type'] = 'application/json'
        return request

    def get_request(self, method='', uri='', params=''):
        """
        :param method:
        :param uri:
        :return:
        """
        params_dict = {}
        if params.find("=") != -1:
            params_dict = dict((k.strip(), v.strip()) for k,v in(item.split('=') for item in params.split('&')))
        elif params != '':
            params_dict = {}
            params_dict[params] = ''
        return {
            'method': method,
            'uri': uri,
            'params': params_dict,
            'headers': {
                'x-bce-date': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                'host': self.service_base_url,
                'content-type': 'application/json'
            }
        }
