#!/usr/bin/env python3

"""
OAuth1 Setup for Jira Rest API Tool Usage


Copyright (c) 2018-2021, sci_Zone, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from ecdsa import SigningKey, NIST384p
import sys
import base64
import importlib
import urllib
import requests
from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1Session
from jira.client import JIRA


def read(file_path):
    """ Read a file and return it's contents. """
    try:
        with open(file_path) as f:
            return f.read()
    except Exception:
        sys.exit(file_path+' not found')
    except:
        sys.exit('Error reading file '+file_path)    
        
print("STEP 1: Enter Consumer Key")
# Step 1: Enter Consumer Key 
while True:
    try:
        CONSUMER_KEY = input('Enter the Consumer Key: ')
        if CONSUMER_KEY:
            print("\n")
            break
        else:
            print('--> NO Entry for the Consumer Key! Retry')
            print("\n")
    except ValueError:
        if not input:
            print('Error entering the Consumer Key') 

print('Step 2: Enter Consumer Secret')
# Step 2: Enter Consumer Secret 
while True:
    try:
        CONSUMER_SECRET = input('Enter the Consumer Secret: ')
        if CONSUMER_SECRET:
            print("\n")
            break
        else:
            print('--> NO Entry for the Consumer Secret! Retry')
            print("\n")
    except ValueError:
        if not input:
            print('Error entering the Consumer Secret') 

#CONSUMER_KEY = 'OauthKey'
#CONSUMER_SECRET = 'qstest'

print('Step 3: Enter the RSA Key File Name (the private RSA key)')
# Step 3: Enter the RSA Key File Name (the private RSA key)
while True:
    try:
        RSA_KEY_FILE = input('Enter the path and filename for the RSA Key file [jira_privatekey.pem]: ')
        if RSA_KEY_FILE:
            print("\n")
            break
        else:
            RSA_KEY_FILE = 'jira_privatekey.pem'
            print("\n")
            break
    except ValueError:
        if not input:
            print('Error with RSA Key File') 

RSA_KEY = read(RSA_KEY_FILE)
#RSA_KEY = read('../../../home/andrewsantangelo/jira_privatekey.pem')

print('Step 4: Enter the Jira server web address')
# Step 4: Enter the Jira server web address 
while True:
    try:
        JIRA_SERVER = input('Enter the Jira Server address [http://jira.quick-sat.com]: ')
        if JIRA_SERVER:
            break
            print("\n")
        else:
            JIRA_SERVER = 'http://jira.quick-sat.com'
            break
            print("\n")
    except ValueError:
        if not input:
            print('Error with Jira Server address entry') 


# The URLs for the JIRA instance
#JIRA_SERVER = 'http://jira.quick-sat.com'
REQUEST_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/request-token'
AUTHORIZE_URL = JIRA_SERVER + '/plugins/servlet/oauth/authorize'
ACCESS_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/access-token'

# Step 5: Get a request token

oauth = OAuth1Session(CONSUMER_KEY, signature_type='auth_header', signature_method=SIGNATURE_RSA, rsa_key=RSA_KEY, verifier=CONSUMER_SECRET)
request_token = oauth.fetch_request_token(REQUEST_TOKEN_URL,verify=True)

print("STEP 5: GET REQUEST TOKEN")
print(" oauth_token={}".format(request_token['oauth_token']))
print(" oauth_token_secret={}".format(request_token['oauth_token_secret']))
print("\n")


# Step 6: Get the end-user's authorization

print("STEP 6: AUTHORIZATION")
print(" Visit to the following URL to provide authorization:")
print(" {}?oauth_token={}".format(AUTHORIZE_URL, request_token['oauth_token']))
print("\n")

destination= open("linkJira.txt","w+")
destination.write(" oauth_token={}".format(request_token['oauth_token']))
destination.write(" oauth_token_secret={}".format(request_token['oauth_token_secret']))
destination.write(" {}?oauth_token={}".format(AUTHORIZE_URL, request_token['oauth_token']))
destination.close()

while input("Press any key to continue..."):
    pass
    
    
# Step 7: Get the access token

access_token = oauth.fetch_access_token(ACCESS_TOKEN_URL)

print("STEP 7: GET ACCESS TOKEN")
print(" oauth_token={}".format(access_token['oauth_token']))
print(" oauth_token_secret={}".format(access_token['oauth_token_secret']))
print("\n")

# Step 8: Test out the Oauth1 Setup


while True:
    try:
        tryit = input("STEP 8: Would you like to test the Oauth1 Setup (y or n)? [y]")
        if (tryit == 'y') or (tryit == 'Y'):
            print("\n")
            break
        elif (tryit == 'n') or (tryit == 'N'):
            quit()
        else:
            break
        print("\n")
    except ValueError:
        quit()

jira = JIRA(options={'server': JIRA_SERVER,'verify':True}, oauth={
'access_token': access_token['oauth_token'],
'access_token_secret': access_token['oauth_token_secret'],
'consumer_key': CONSUMER_KEY,
'key_cert': RSA_KEY
})

for project in jira.projects():
    print(project.key)
