"""
Core Test Class for QS_Test


Copyright (c) 2018-2022, sci_Zone, Inc.
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


class qs_test:

        def __init__(self):
            print('test start')


if __name__ == '__main__':

    authorization = ('auser','apassword')
    myTest = synapsert.synapsert()
    
    print('Get Immediate Child Requirements')
    resp, respj = myTest.get_immediate_child_requirements('http://localhost:8080',authorization,'VSMFSW-1090')
    print(resp.status_code)
    for thecycles in respj:
        print(thecycles)

    print('Get ALL Child Requirements')
    resp, respj = myTest.get_all_child_requirements('http://localhost:8080',authorization,'VSMFSW-1090')
    print(resp.status_code)
    for thecycles in respj:
        print(thecycles)
        
        
        