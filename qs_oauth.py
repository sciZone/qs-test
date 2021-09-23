#!/usr/bin/env python3

from ecdsa import SigningKey, NIST384p
import base64
import importlib
import urllib
import requests
import sys
import os
import os.path
import socket
import time
import timeit
import getopt
from tempfile import mkstemp
try:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
    from http.server import HTTPServer, SimpleHTTPRequestHandler

from tlslite import TLSConnection, Fault, HandshakeSettings, \
    X509, X509CertChain, IMAP4_TLS, VerifierDB, Session, SessionCache, \
    parsePEMKey, constants, \
    AlertDescription, HTTPTLSConnection, TLSSocketServerMixIn, \
    POP3_TLS, m2cryptoLoaded, pycryptoLoaded, gmpyLoaded, tackpyLoaded, \
    Checker, __version__
from tlslite.handshakesettings import VirtualHost, Keypair

from tlslite.utils.cryptomath import prngName, getRandomBytes
from tlslite.utils import keyfactory
from urllib.parse import urlparse
import oauth2 as oauth

from tlslite.utils.cryptomath import prngName, getRandomBytes
try:
    import xmlrpclib
except ImportError:
    # Python 3
    from xmlrpc import client as xmlrpclib
import ssl
from tlslite import *
import tlslite.utils as secure1
from requests_oauthlib import OAuth1


class SignatureMethod_RSA_SHA1(oauth.SignatureMethod):
    name = 'RSA-SHA1'

    def signing_base(self, request, consumer, token):
        if not hasattr(request, 'normalized_url') or request.normalized_url is None:
            raise ValueError("Base URL for request is not set.")

        sig = (
            oauth.escape(request.method),
            oauth.escape(request.normalized_url),
            oauth.escape(request.get_normalized_parameters()),
        )

        key = '%s&' % oauth.escape(consumer.secret)
        if token:
            key += oauth.escape(token.secret)
        raw = '&'.join(sig)
        return key, raw

    def sign(self, request, consumer, token):
        """Builds the base signature string."""
        key, raw = self.signing_base(request, consumer, token)
        raw = bytes(raw, 'utf8')
        print('********')

        print(raw)
        print('********')
        with open('../../../home/andrewsantangelo/jira_privatekey.pem', 'r') as f:
            data = f.read()
        privateKeyString = data.strip()

        print(privateKeyString)
        privatekey = secure1.keyfactory.parsePrivateKey(privateKeyString)
        print('-----------')
        print(privatekey)
        print('-----------')
        signature = privatekey.hashAndSign(raw)
        print(signature)

        return base64.b64encode(signature)

if __name__ == '__main__':

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    print('Begin OAuth Operation')
    
    consumer_key = 'OauthKey'
    consumer_secret = 'qstest'

    request_token_url = 'http://jira.quick-sat.com/jira/plugins/servlet/oauth/request-token'
    access_token_url = 'http://localhost:8080/jira/plugins/servlet/oauth/access-token'
    authorize_url = 'http://localhost:8080/jira/plugins/servlet/oauth/authorize'
    #authorize_url = 'http://jira.quick-sat.com/plugins/servlet/oauth/authorize'
    
    
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)
    print(consumer)
    print(client)
    host_url='http://localhost:8080'
    url_api = host_url+'/rest/synapse/latest/public/testPlan/TPX-15/cycle/7/testRunsByCycleId'
    authorization = ('spacetravelerx','spacey')
    #authorization = OAuth1('OauthKey', 'qstest', 'd00VO6', 'xzeapuQ4aZhKUovH9dMZCo1qDv57mZ9g')
    
    
    resp = requests.get(url=url_api, auth=authorization)
    print(resp.status_code)
    if resp.status_code != 401:
        respj = resp.json()
        for thesummary in respj:
            print(thesummary) 
        
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)        
    client.set_signature_method(SignatureMethod_RSA_SHA1())
    
    resp, content = client.request(request_token_url, "POST")
    print(resp['status'])
    print(content)
    #if resp['status'] != '200':
    #    raise Exception("Invalid response %s: %s" % (resp['status'],  content))
        
    request_token = dict(urllib.parse.parse_qsl(content))
    print(request_token)

    oauth_token = request_token['oauth_token']
    oauth_token_secret = request_token[b'oauth_token_secret']
