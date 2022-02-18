#!/usr/bin/env python3

"""
Callable Test Recorder for the qs_test environment.  This application
     assumes Jira/SynapseRT are used to store the test results.
     
This function will also, if requested, automatically zip a directory that is to be saved

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
    parser.add_argument ('--n', type=str, help='Test case name (string)', default = None)
    parser.add_argument ('--r', type=str, help='The Result to post to the test case. Allowable values: "Passed","Failed","Blocked","Not Tested","NA', default = None)
    parser.add_argument ('--c', type=str, help='Comment to post for the test case', default = None)
    parser.add_argument ('--f', type=str, help='The file and directory location of the test case results to be stored', default = None)
    parser.add_argument ('--d', type=str, help='The directory of the test case files to be zipped and be stored', default = None)

     args, unknown = parser.parse_known_args()

     return args, unknown


if __name__ == '__main__':
    args, unknown = parse_args()

    print(unknown)
    print(args)
    print('Test name is ' + args.a + ', the result is '+ args.r + 'the comment is '+ args.c)
    print('The file to store is ' + args.f)
    print('The file to store is ' + args.d)
     
    #
    # check if test case ('n') is provided.  If not, exit the app
    #
    if ( args.n is None):
        print('--> No Test Case name was given')
        print('--> Exiting qs_tes_recorder_srt')
        sys.exit()
    
    reportZip = shutil.make_archive(args.d, 'zip', args.d)
    print('Storing results of test...')
    print(reportZip)
    theZipFile = args.dir+'.zip'
    print(theZipFile)
    myTest = qs_test.qs_test()   # Creating new instance of qs_test Class
    try:
        myTest.qst_result_srt(args.n, args.r, args.c)
        myTest.qst_store_log_srt(testCase, theZipFile)
    except:
        print('**** Accessing QS_TEST Failed ****')
        sys.exit()