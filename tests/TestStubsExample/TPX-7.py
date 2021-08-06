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
    
    json_actual = {
                     'temperature' : 331.4,
                     'pressure' : 10001.0,
                     'sensor_1' : True,
                     'sensor_2' : False,
                     'sensor_6' : False
    }
    
    
    json_expected = {
                     'sensor_1' : True,
                     'temperature' : 331.4,
                     'pressure' : 10001.0,
                     'sensor_2' : False,
                     'sensor_6' : True
    }
    
    jsonA = json.dumps(json_actual, sort_keys=True)
    jsonE = json.dumps(json_expected, sort_keys=True)
    
    print(jsonA == jsonE)
    
    try: 
        myMainTest.qst_test_srt(testCaseKey,json_expected,json_actual,'The values match!','There was an error in the test')  
        
        myMainTest.qst_store_log_srt(testCaseKey,'qs_test_results.log')
        
    except:
    
        print('Failure using qs_test library')
    
    

