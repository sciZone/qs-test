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
import argparse
import configparser


import jira_rest_api
import synapsert
import qs_test



if __name__ == '__main__':

    
    testCaseKey = os.path.splitext(os.path.basename(__file__))[0]
    
    print('The Test is: '+ os.path.splitext(os.path.basename(__file__))[0])

    myMainTest = qs_test.qs_test()

    
    try: 
    
        myMainTest.qst_result_srt(testCaseKey, 'Blocked', 'Test stub for test case '+testCaseKey)

        myMainTest.qst_store_log_srt(testCaseKey,'qs_test_results.log')
        
    except:
    
        print('Failure using qs_test library')
    
    

