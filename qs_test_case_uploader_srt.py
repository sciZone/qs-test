#!/usr/bin/env python3
"""
Application to Upload Test Cases to Jira/Testray and link to a Test Suite and/or a Requirement if they are given


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
# function parse_args: This Function takes developed test case(s) from designed_testcases.json, uploads them
#                      to Jira/Testray, links the test case(s) to a designated Test Suite if defined, and links 
#                      test case(s) to a designated Requirement if defined
#
# @return: Jira based testCaseKeys
#

def parse_args():
    parser = argparse.ArgumentParser(description='Load qs-test parameters', conflict_handler='resolve')
    parser.add_argument ('--Project', type=str, help='Jira Project to link Test Case(s) to', default = None)
    parser.add_argument ('--RequirementKey', type=str, help='Requirement Key to link Test Case(s) to', default = None)
    parser.add_argument ('--TestSuite', type=str, help='Test Suite to link the Test Case(s) to', default = "-NA-")

    args, unknown = parser.parse_known_args()

    return args, unknown


if __name__ == '__main__':

    args, unknown = parse_args()

    qst_home = os.getenv('QT_HOME','')

    myTest = qs_test.qs_test()   # Creating new instance of qs_test Class

    #
    # check if 'Project' is provided.  If not, exit the app
    #
    if ( args.Project is None):
    
        if myTest.qt_log: myTest.logging.warning("* qs_test_case_uploader_srt: No Jira Project was given")
        if myTest.qt_log: myTest.logging.warning("* qs_test_case_uploader_srt: Exiting QS Test Case Upload")
        sys.exit()
    else:
        projectKey = args.Project
        
    # Retrieve the file designed_testcases.json containing the designed test case(s)

    # Define the path to the JSON file
    # First check if QT_CONFIG environment variable is set

    qt_config = os.environ.get('QT_CONFIG', '')

    if qt_config:
        # Use environment variable path
        json_file_path = os.path.join(qt_config, 'designed_testcases.json')
    else:
        # Default to local directory structure
        json_file_path = os.path.join('qs-test', 'config', 'designed_testcases.json')

    try:
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            test_case_data = json.load(file)
        print(f"Successfully loaded test cases from {json_file_path}")
        print(f"Number of test cases: {len(test_case_data.get('test_cases', []))}")
        
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        test_case_data = {"test_cases": []}  # Initialize with empty array
        
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        test_case_data = {"test_cases": []}  # Initialize with empty array
        
    except Exception as e:
        print(f"Error loading test cases: {str(e)}")


 #
 #  Upload designed test case(s) to Jira/Testray
 # 
 #  
 
    testCaseKeys = myTest.qst_upload_test_cases_srt(test_case_data)

    # print(testCaseKeys) 

    #
    # Check if a Test Suite is given. If there is a Test Suite, link the Test Case(s) to the Test Suite
    #

    if (args.TestSuite is not None):
        try:
            resp = myTest.qst_link_test_cases_test_suite_srt(projectKey, args.TestSuite, testCaseKeys)
        except:
            myTest.logging.warning("* qs_test_case_uploader_srt: Error Linking Test Cases to the Test Suite: "+args.TestSuite)
            myTest.logging.warning("* qs_test_case_uploader_srt: Exiting qs_test_upload_srt")
            sys.exit()
   

    #
    # Check if Requirement is Given. If there is a Requirement, link the Test Case(s) to the Requirement
    #

    if (args.RequirementKey is not None):
        # Format for Testray
        test_case_list = { 
                           "testCaseKeys": testCaseKeys
            }
        try: 
            resp = myTest.qst_link_test_cases_requirement_srt(args.RequirementKey, test_case_list)
        except:
            myTest.logging.warning("* qs_test_case_uploader_srt: Error Linking Test Cases to the Requirement: "+args.RequirementKey)
            myTest.logging.warning("* qs_test_case_uploader_srt: Exiting qs_test_upload_srt")
            sys.exit()
 



