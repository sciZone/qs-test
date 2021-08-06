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

    myMainTest = qs_test.qs_test()
    
    testCaseKey = os.path.splitext(os.path.basename(__file__))[0]
    
    print('The Test is: '+ os.path.splitext(os.path.basename(__file__))[0])
    
    try: 
    
        myMainTest.qst_result_srt(testCaseKey, 'Failed', 'Test stub for test case '+testCaseKey)
        
    except:
    
        print('Failure using qs_test library')
    
    

