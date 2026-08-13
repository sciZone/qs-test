#!/usr/bin/env python3

"""
Core Test Class for Jira Rest API Tool


Copyright (c) 2018-2026, sci_Zone, Inc.

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

import syslog
import subprocess
import time
import traceback
import sys
import os
import errno
import requests
import mimetypes 
import json


class jira_rest(object):
    """
    A class that handles Jira REST APIs
    """
    def __init__(self):
        self.db_args = None

    def __del__(self):
        pass

#
#   Function manages GET REST APIs
#

    def api_request_get(self, url_api, authorization, verifyFile=False):

        try:
            #print(url_api)
            resp = requests.get(url=url_api, headers=authorization, verify=verifyFile)
            return resp
            
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

#
#   Function manages POST REST APIs
#
 
    def api_request_post(self, url_api, data_api, authorization, verifyFile=False):

        try:
            resp = requests.post(url=url_api, headers=authorization, json=data_api, verify=verifyFile)
            return resp
            
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

#
#   Function manages POST REST APIs specific to uploading a file
#
 
    def api_request_post_upload_file(self, url_api, file_path_info, authorization, verifyFile=False):


        try:
            mime_type, encoding = mimetypes.guess_file_type(file_path_info)
        except AttributeError:
            mime_type, encoding = mimetypes.guess_type(file_path_info)

        try:
            files={'file': (file_path_info, open(file_path_info, 'rb'), mime_type,)}
            
            #print()
            #print(files)
            #print(mime_type)
            #print(url_api)
            #print(authorization)
            resp = requests.post(url=url_api, headers=authorization, files=files, verify=verifyFile)
            #print(resp)
            return resp
            
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
            
            
#
#   Function manages PUT REST APIs
#
 
    def api_request_put(self, url_api, data_api, authorization, verifyFile=False):

        try:
            headers={
                'Content-type':'application/json', 
                'Accept':'application/json'
            }
            resp = requests.put(url=url_api, headers=headers, json=data_api, auth=authorization, verify=verifyFile)
            return resp
            
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

#
#   Function manages DELETE REST APIs
#
 
    def api_request_delete(self, url_api, data_api, authorization, verifyFile=False):

        try:
            headers={
                'Content-type':'application/json', 
                'Accept':'application/json'
            }
            resp = requests.delete(url=url_api, headers=headers, json=data_api, auth=authorization, verify=verifyFile)
            return resp
            
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

