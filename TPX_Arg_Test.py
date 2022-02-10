#!/usr/bin/env python3

'''
Making a basic qs-test runner that accepts the test case and a directory path as parameters
'''



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
# function parse_args: This function gets the test case name and the log directory path and
#                      returns them as a tuple.
# @return: (<test_case_name>, <log_directory_path>)
#

def parse_args():
     parser = argparse.ArgumentParser(description='Load qs-test parameters', conflict_handler='resolve')
     parser.add_argument ('--name', type=str, help='Test case name (string)', default='TPX-10')
     parser.add_argument ('--dir', type=str, help='Directory path for CTF log', default='log')
     args, unknown = parser.parse_known_args()

     return args, unknown


if __name__ == '__main__':
     args, unknown = parse_args()
     print(unknown)
     print(args)
     print('Test name is ' + args.name + ', directory is ' + args.dir)
     print('Zipping up directory...')
     reportZip = shutil.make_archive(args.dir, 'zip', args.dir)
     print('Storing results of test...')
     print(reportZip)
     theZipFile = args.dir+'.zip'
     print(theZipFile)
     myTest = qs_test.qs_test()
     testCase = args.name
     try:
         myTest.qst_result_srt(testCase, 'Passed', 'Test stub for test case '+testCase)
         myTest.qst_store_log_srt(testCase, theZipFile)
     except:
         print('**** Accessing QS_TEST Failed ****')
         pass