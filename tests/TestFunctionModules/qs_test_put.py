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


class qs_test_put:

        def __init__(self):
            print('test start')


if __name__ == '__main__':

    authorization = ('spacetravelerx','spacey')
    myTest = synapsert.synapsert()

    print(' ')
    resp = myTest.update_test_cycle('http://localhost:8080',authorization,'TPX-15', 'TPBX Phase B2','Resume')
    print(resp.status_code)

