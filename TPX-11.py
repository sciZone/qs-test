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

import codecs
import shlex
import getpass
import datetime
import logging

import shutil
import jira_rest_api
import synapsert
import qs_test


if __name__ == '__main__':

    myMainTest = qs_test.qs_test()
    
    testCaseKey = os.path.splitext(os.path.basename(__file__))[0]
    
    print('The Test is: '+ os.path.splitext(os.path.basename(__file__))[0])
    
    logDirectory = testCaseKey+'_log'
    print('Test name is ' + testCaseKey + ', directory is ' + logDirectory)
    
    if not os.path.isdir(logDirectory):
        print("Error: path is not directory")
        raise NotADirectoryError
    
        
    print('Zipping up directory...')
    reportZip = shutil.make_archive(logDirectory, 'zip', logDirectory)
    print('Storing results of test...')
    print(reportZip)
    theZipFile = logDirectory+'.zip'
    print(theZipFile)    
    
    try: 
    
        myMainTest.qst_result_srt(testCaseKey, 'Passed', 'Test stub for test case '+testCaseKey)
        myMainTest.qst_store_log_srt(testCaseKey, theZipFile)
        
    except:
    
        print('Failure using qs_test library')
    
    

