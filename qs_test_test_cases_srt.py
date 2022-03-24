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

#
# function parse_args: This function gets the test case name and results to post to 
#                      the SynapseRT related test case ANDreturns them as a tuple.
# @return: (<test_case_name>, <log_directory_path>)
#

def parse_args():
    parser = argparse.ArgumentParser(description='Load qs-test parameters', conflict_handler='resolve')
    parser.add_argument ('--tpid', type=str, help='Test Test Plan ID (string)', default = None)
    parser.add_argument ('--cid', type=str, help='Test Cycle ID (string)', default = None)

    args, unknown = parser.parse_known_args()

    return args, unknown



if __name__ == '__main__':

    args, unknown = parse_args()

    myTest = qs_test.qs_test()   # Creating new instance of qs_test Class    
    
    cert_file = False
    
    #
    # Post test result 
    #
    
    
    if (args.tpid and not args.cid):
        myTest.logging.warning("* qs_test_test_cases_srt: Entered Test Plan ID, but missing the Test Cycle ID")
        myTest.logging.warning("* qs_test_test_cases_srt: Exiting qs_test_test_cases_srt")
        sys.exit()

    if (not args.tpid and args.cid):
        myTest.logging.warning("* qs_test_test_cases_srt: Entered Test Cycle ID, but missing the Test Plan ID")
        myTest.logging.warning("* qs_test_test_cases_srt: Exiting qs_test_test_cases_srt")
        sys.exit()

    try:
    
        result = myTest.qst_get_test_case_set(args.tpid, args.cid)

    except:
        myTest.logging.warning("* qs_test_test_cases_srt: Error getting test cases for given Test Plan ID AND Test Cycle ID")
        myTest.logging.warning("* qs_test_test_cases_srt: Exiting qs_test_test_cases_srt")
        sys.exit()  



    
