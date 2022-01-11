#!/usr/bin/env python3

"""
Tool to search orphaned requirements


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
        
        
#
# Have user select credentials OR to use Oauth1
#

while True:
    try:
        login_method = input('Select O(auth) or C(redentials):')
        if login_method and ( login_method.upper()=='O' or login_method.upper()=='C'):
            print("\n")
            break
        else:
            print('--> INVALID Entry for the Login Method Type! Retry')
            print("\n")
    except ValueError:
        if not input:
            print('Error entering the Consumer Key') 

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


#JIRA_SERVER = 'http://jira.quick-sat.com'
#RSA_KEY_FILE = 'jira_privatekey.pem'
#CONSUMER_KEY = 'OauthKey'
#req_substring = 'L4-'

print('Step 2: Enter the RSA Key File Name (the private RSA key)')
# Enter the RSA Key File Name (the private RSA key)
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

print('Step 3: Enter the Jira server web address')
#  Enter the Jira server web address 
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


print('Step 4: Enter the \"L\" type requirement to enter')
while True:
    try:
        req_substring = input('Enter the \"L\" type requirement followed by a \"-\" [L4-]: ')
        if req_substring:
            print("\n")
            break
        else:
            req_substring = 'L4-'
            print("\n")
            break
    except ValueError:
        if not input:
            print('Error with Requirement type entered') 



RSA_KEY = read(RSA_KEY_FILE)

jira = JIRA(options={'server': JIRA_SERVER,'verify':True}, oauth={
'access_token': 'COGHeQiuPfCHnzyRjoqVJJo8ZIaPs2Zd',
'access_token_secret': '3QT3Xj1KBGgdHPzteERQMHZGm0ZvfYvA',
'consumer_key': CONSUMER_KEY,
'key_cert': RSA_KEY
})

    
l4_req_count = 0
l4_orphan_count = 0
for issues_found in jira.search_issues('project=VSMFSW'):

    if issues_found.fields.customfield_10105:
        if req_substring in issues_found.fields.customfield_10105:
            l4_req_count = l4_req_count + 1
            if issues_found.fields.customfield_10106:
                print('{}: {}, Parent Requirement ID: {}, Requirement ID: {}'.format(issues_found.key, issues_found.fields.summary, issues_found.fields.customfield_10106, issues_found.fields.customfield_10105))
            else:
                print('{}: {}, ORPHAN, Requirement ID: {}'.format(issues_found.key, issues_found.fields.summary, issues_found.fields.customfield_10105))
                l4_orphan_count = l4_orphan_count + 1

print("\n")
print("Total \""+ req_substring+"\" Requirements: " + str(l4_req_count))
print("Total Orphaned \""+req_substring+"\" Requirements: " + str(l4_orphan_count))

