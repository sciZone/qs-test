#!/usr/bin/env python3

"""
Core Test Class for QS_Test_Post


Copyright (c) 2018-2021, sci_Zone, Inc.
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
from atlassian import Jira
from atlassian import Confluence

import jira_rest_api
import synapsert


class qs_test_post:

        def __init__(self):
            print('test start')


if __name__ == '__main__':

    cert_data=False
    authorization = ('spacetravelerx','spacey')
    myTest = synapsert.synapsert()
    test_run_data = { 
          "name": "test2", "environment":"QS_TEST", "build":"Version Test", "plannedStartDate":"2017-04-13", "plannedEndDate":"2017-04-15"
    }
    resp = myTest.add_test_cycle('http://localhost:8080',authorization, "TPX-15", test_run_data, cert_data)
    print(resp.status_code)

