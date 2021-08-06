#!/usr/bin/env python3

"""
Core Test Class for QS_Test


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


class qs_test:

        def __init__(self):
            print('test start')


if __name__ == '__main__':

    authorization = ('spacetravelerx','spacey')
    myTest = synapsert.synapsert()
    
    print('Get Test Cycles')
    resp, respj = myTest.get_test_cycles('http://localhost:8080',authorization,'TPX-15')
    print(resp.status_code)
    for thecycles in respj:
        print(thecycles)
        print(thecycles['cycleName'])
        print(thecycles['id'])
        
    print(' ')
    print('Test Run Details')
    resp, respj = myTest.get_test_run_details('http://localhost:8080',authorization,'7')
    print(resp.status_code)
    for thesummary in respj['testRunDetails']:
        print(thesummary)
        
    print(' ')
    print('Test Cases')
    resp, respj = myTest.get_test_cases('http://localhost:8080',authorization,'TPX-15')
    print(resp.status_code)
    for thesummary in respj:
        print(thesummary)
        
    print(' ')
    print('Get Run Details Cases')
    resp, respj = myTest.get_run_details_cases('http://localhost:8080',authorization,'TPX-15')
    print(resp.status_code)
    for thesummary in respj['testCycles']:
        print(thesummary)
        print(thesummary['testCycleName'])
        
    print(' ')
    print('Defects in Plan')
    resp, respj = myTest.get_defects_plan('http://localhost:8080',authorization,'TPX-15')
    print(resp.status_code)
    for thesummary in respj:
        print(thesummary)
       
    print(' ')
    print('Get Test Runs')
    resp, respj = myTest.get_test_runs('http://localhost:8080',authorization,'TPX-15', 'TPBX Phase B3')
    print(resp.status_code)
    for thesummary in respj:
        print(thesummary) 
        
    print(' ')
    print('Get Test Runs, ID='+'7')
    resp, respj = myTest.get_test_runs_by_id('http://localhost:8080',authorization,'TPX-15', '7')
    print(resp.status_code)
    for thesummary in respj:
        print(thesummary) 

    print(' ')
    print('Get Defects By ID=7')
    resp, respj = myTest.get_cycle_defects_by_id('http://localhost:8080',authorization,'TPX-15', '7')
    print(resp.status_code)
    for thesummary in respj:
        print(thesummary) 
        
    print(' ')
    print('Get Steps Test Case = TPX-16')
    resp, respj = myTest.get_steps_test_case('http://localhost:8080',authorization,'TPX-16')
    print(resp.status_code)
    for thesummary in respj:
        print(thesummary) 

    print(' ')
    print('Get Attachement Details Run ID 58')
    resp, respj = myTest.get_attachment_details_test_run('http://localhost:8080',authorization,'58')
    print(resp.status_code)
    for thesummary in respj:
        print(thesummary) 

