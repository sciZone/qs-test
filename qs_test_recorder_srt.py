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
    parser.add_argument ('--cm', type=str, help='Comment to post for the test case', default = "-NA-")
    parser.add_argument ('--f', type=str, help='The file and directory location of the test case results to be stored', default = None)
    parser.add_argument ('--d', type=str, help='The directory of the test case files to be zipped and be stored', default = None)

    args, unknown = parser.parse_known_args()

    return args, unknown


if __name__ == '__main__':
    args, unknown = parse_args()

    myTest = qs_test.qs_test()   # Creating new instance of qs_test Class
    
    #print(unknown)
    #print(args)
    #print('Test name is ' + str(args.n) + ', the result is '+ str(args.r) + ', the comment is '+ str(args.cm))
    #print('The file to store is ' + str(args.f))
    #print('The director to zip and store is ' + str(args.d))
     
    #
    # check if test case ('n') is provided.  If not, exit the app
    #
    if ( args.n is None):
    
        if myTest.qt_log: myTest.logging.warning("* qs_test_recorder_srt: No Test Case name was give")
        if myTest.qt_log: myTest.logging.warning("* qs_test_recorder_srt: Exiting qs_tes_recorder_srt")
        sys.exit()
        
    #
    # Post test result 
    #
    try:
        if (args.r is None):
            myTest.qst_result_srt(args.n, 'NA', args.cm)
        else:
            myTest.qst_result_srt(args.n, args.r, args.cm)
    except:
        myTest.logging.warning("* qs_test_recorder_srt: Error posting result and comment")
        myTest.logging.warning("* qs_test_recorder_srt: Exiting qs_test_recorder_srt")
        sys.exit()     
        
    #
    # Check if file is given. If there is a file upload the file to SynapseRT
    #
    if (args.f is not None):
        try:
            myTest.qst_store_log_srt(args.n, args.f)
        except:
            myTest.logging.warning("* qs_test_recorder_srt: Error Saving the file given")
            myTest.logging.warning("* qs_test_recorder_srt: Exiting qs_test_recorder_srt")
            sys.exit()
  
    #
    # check if directory ('d') is provided.  If yes, exit the zip the directory
    #
    if (args.d is not None):
        try:
            reportZip = shutil.make_archive(args.d, 'zip', args.d)
    #       print('Storing results of test...')
    #       print(reportZip)
            theZipFile = args.d+'.zip'
    #       print(theZipFile)
            myTest.qst_store_log_srt(args.n, theZipFile)
        except:
            myTest.logging.warning("* qs_test_recorder_srt: Error zipping the directory given")
            myTest.logging.warning("* qs_test_recorder_srt: Exiting qs_test_recorder_srt")
            sys.exit()

    myTest.logging.info("* qs_test_recorder_srt: Recording results for Test Case "+args.n+" is completed")

