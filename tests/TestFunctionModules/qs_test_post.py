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

    authorization = ('spacetravelerx','spacey')
    myTest = synapsert.synapsert()
    test_run_data = { 
          "runStepId": 2, "result":"Blocked", "actualResult":"This Test Step is failed.", "bugs":[]
    }
    runID = '7'
    resp = myTest.update_test_run_step('http://localhost:8080',authorization, runID, test_run_data)
    print(resp.status_code)

