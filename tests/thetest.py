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
        if not hasattr(request, 'normalized_url') \
                or request.normalized_url is None:
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
        """Build the base signature string."""
        key, raw = self.signing_base(request, consumer, token)
        raw = bytes(raw, 'utf8')
        with open(RSA_PEM_FILEPATH, 'r') as rsa_file:
            data = rsa_file.read()
        private_key_string = data.strip()
        private_key = keyfactory.parsePrivateKey(private_key_string)
        signature = private_key.hashAndSign(raw)
        return base64.b64encode(signature)


# Replace with the path to your RSA .pem file
RSA_PEM_FILEPATH = '../../../home/andrewsantangelo/jira_privatekey.pem'

# Replace with your own consumer key and shared secret
CONSUMER_KEY = 'OauthKey'
CONSUMER_SECRET = 'qstest'

# Replace with the URL for your JIRA instance (include the end slash!)
JIRA_URL = 'http://localhost:8080/jira/'

# Replace with the ID of a new issue you can use for testing
NEW_ISSUE = 'TPX-17'

REQUEST_TOKEN_URL = JIRA_URL + 'plugins/servlet/oauth/request-token'
ACCESS_TOKEN_URL = JIRA_URL + 'plugins/servlet/oauth/access-token'
AUTHORIZE_URL = JIRA_URL + 'plugins/servlet/oauth/authorize'
DATA_URL = JIRA_URL + 'rest/api/2/issue/' + NEW_ISSUE

consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client = oauth.Client(consumer)
print(client)

# Let's try to access a JIRA issue (NEW_ISSUE). We should get a 401.
resp = client.request(DATA_URL, "GET")
if resp['status'] != '401':
    raise Exception("Should have no access!")

consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client = oauth.Client(consumer)
#client.set_signature_method(SignatureMethod_RSA_SHA1())