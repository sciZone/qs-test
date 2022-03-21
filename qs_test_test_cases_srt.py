#!/usr/bin/env python3

"""
Callable Test Case Information for the qs_test environment.  This application
     assumes Jira/SynapseRT are used to store the test results.
     
results are stored in the directory 'config' in the file names 'test_case_list.jsonup'
    

--------------------------------------------------------------------------

Copyright (c) 2018-2022, sci_Zone, Inc.

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
import json

import codecs
import shlex
import getpass
import datetime
import logging
import argparse
import configparser


import jira_rest_api
import synapsert
import qs_test


import argparse
import shutil




if __name__ == '__main__':


    myTest = qs_test.qs_test()   # Creating new instance of qs_test Class    
    
    cert_file = False

    result = myTest.qst_get_test_case_set()

    
