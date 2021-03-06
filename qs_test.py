#!/usr/bin/env python3

"""
Core Test Class for QS_Test


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
import glob

import codecs
import shlex
import getpass
import datetime
import logging
import argparse
import configparser

# Fernet is a system for symmetric encryption/decryption

from cryptography.fernet import Fernet

import jira_rest_api
import synapsert


#
#
# function get_fernet:  This function gets the "key" from the key file to decipher the encrypted password
#
#           key_file = the filename storing the key for the file to be decrypted

def get_fernet(qs_home, key_file):
    with open(f""+qs_home+"config/."+key_file, "rb") as f:
        cipher = Fernet(f.read())

    return cipher


#
#
# function parse_args:  This function allows the "config" information and the current QuickSAT information
#                       to be loaded into the QuickSAT Environment
#
#

def parse_args(qs_home):
    parser = argparse.ArgumentParser(description='Load QuickSAT Data.')
    parser.add_argument('--config',
                        help='Configuration to use.',
                        default= 'qs_default')
    args, unknown = parser.parse_known_args()

    return args



#   
#    Exception Class for qs_test class of functions
#
class QSTError(Exception):
    pass


class qs_test(object):

    def __init__(self):
        
        
        #
        #  Get the path to the home directory if it exists
        #
        
        self.qst_home = os.getenv('QT_HOME','')
        
        #
        #  Get Configuration information
        #
        args = parse_args(self.qst_home)              # Define args


        #  Read the configuration information specific to the QuickSAT Environment
        config = __import__(f'config.{args.config}', fromlist=['ENV_CONFIG', 'DATABASE_CONFIG'])

        self.auth_url = config.ENV_CONFIG.get('AUTH_URL', None)
        self.qs_url = config.ENV_CONFIG.get('QS_URL', None)
        self.jira_url = config.ENV_CONFIG.get('JIRA_URL', None)
        self.jira_user = config.ENV_CONFIG.get('JIRA_USER', None)
        self.cert_file = config.ENV_CONFIG.get('CERT_FILE', None)
        self.qt_synapsert = config.ENV_CONFIG.get('QT_SYNAPSERT', False)
        self.qt_log = config.ENV_CONFIG.get('QT_LOG', False)
        self.qt_log_flush = config.ENV_CONFIG.get('QT_LOG_FLUSH', False)        
        self.qt_log_display = config.ENV_CONFIG.get('QT_LOG_DISPLAY', False)
        self.qt_log_append = config.ENV_CONFIG.get('QT_LOG_APPEND', False)
        self.qs_user = config.ENV_CONFIG.get('QS_USER', None)
        
        qspass_file = config.ENV_CONFIG.get('QS_PASSSFILE', None)
        if qspass_file == None:
            self.qs_pass_file = f""+self.qst_home+"config/.qsjirapassfile"
        else:
            self.qs_pass_file = qspass_file


        # 
        #  Remove ALL old log files IF qt_log_flush is enabled
        #
        
        if self.qt_log_flush and not self.qt_log_append:
            # Get a list of all the QST_Run_* log files
            
            qt_fileList = glob.glob(self.qst_home+'log/QST_Run_*')
            qst_run_log  = 'QST_Run_*'

            # Iterate over the list of filepaths & remove each file.
            for filePath in qt_fileList:
                try:
                    os.remove(filePath)
                except:
                    print("Error while deleting file : ", filePath)
        

        # 
        #  Set up log file IF enabled
        #

        if self.qt_log:

            self.logging = self.__init_logging(self.qst_home, self.qt_log_display, self.qt_log_append, self.qt_log_flush)    
            dt = str(datetime.datetime.now())
            self.logging.info("------ Start Testing: "+dt)
            
        #  Get user authorization information
        
        self.get_token(self.qst_home)

        #
        #  Get current test plan info
        #
        
        # Verify the file config/test_info.json exists. If not quit test...
        
        try:
            with open(self.qst_home+'config/test_info.json', 'r') as f:
                self.test_info_dict = json.load(f)
                
            # Verify the Test Plan exists
            
            # Get the Test cycles for the Test Plan if the status code is NOT 200
            #   then the Test Plan does not exist and report the error
            testSet = synapsert.synapsert()
            
            try:
                resp, respj = testSet.get_test_cycles(self.jira_url,self.authorization,self.test_info_dict['test_plan_key'], self.cert_file)
            except:    #  If the authorization fails the function will fail
                if self.qt_log: self.logging.warning("> INVALID USERNAME -> "+self.test_info_dict['username'])
                sys.exit()
            
            if resp.status_code == 200:     # This means the Test Plan was found
            
                if self.qt_log: logging.info("> Test Plan : "+self.test_info_dict['test_plan_key'])
            
                # Verify the Test Cycle exists and it is ACTIVE
                cycle_active = False
                cycle_exists = False
                cycleState = ''
                for thecycles in respj:
                    if thecycles['cycleName'] == self.test_info_dict['testCycleName']:
                        cycle_exists = True
                        if cycle_exists and thecycles['status'] == 'Active':
                            cycle_active = True
                        else:
                            cycle_active = False
                            cycleState = thecycles['status']
                    
                
                if cycle_exists and cycle_active:
                    if self.qt_log: logging.info("> Test Cycle Name : "+self.test_info_dict['testCycleName'])
                else:
                    if not cycle_exists:
                        if self.qt_log: self.logging.warning("> Test CYCLE NOT FOUND -> "+self.test_info_dict['testCycleName'])
                        sys.exit()
                    else:
                        if self.qt_log: self.logging.warning("> Test CYCLE "+self.test_info_dict['testCycleName']+ ' FOUND, but STATUS is '+cycleState)
                        sys.exit()
            
            else:   #  Test plan was not found.  Log and exit
            
                if self.qt_log: self.logging.warning("> QS_TEST, INIT: ERROR from getting Test Cycles -> "+str(resp.status_code))
                sys.exit()
            
        except FileNotFoundError as fnfe:
            raise QSTError(fnfe)
            
    def __init_logging(self, qst_home, displayLog, logappend, logflush):
        timestamp = datetime.datetime.now().strftime("QST_Run_%Y_%m_%d_%H_%M_%S")
    
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        
        if logappend:
            # get most recent QST_Run log file
            list_of_log_files = glob.glob(qst_home+'log/QST_Run*') # * means all if need specific format then *.csv
            qt_latest_log_file = max(list_of_log_files, key=os.path.getctime)
            print(qt_latest_log_file)
            fh = logging.FileHandler(qt_latest_log_file)
        else:
            fh = logging.FileHandler(qst_home+'log/'+timestamp)
            
        formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        if displayLog:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        
        logger.addHandler(fh)
        logger.info('Begin logging test run')
        return logger
        
    def __get_pass(self): 

        # get the token
        key_file = "qsjira_key"
        self.__cipher = get_fernet(self.qst_home,key_file)
        
        # Extract the halo Password from the .qsjira_key
        #    The password must also be decoded from "utf-8"
        with open(self.qs_pass_file, 'rb') as pf:
            self.__qsjira_password = self.__cipher.decrypt(pf.read()).decode()
            self.logging.info("User Password found and extracted")
            


    
    def get_token(self, qs_home):
 
        if self.auth_url == None:
            raise QSTError('Authentication URL not defined.')

        if self.jira_user == None:
            if self.prompt:
                self.jira_user = input('Please enter Jira User name : ')

            else:
                raise QSTError('Jira User not defined.')

        if not os.path.exists(self.qs_pass_file):
            if self.prompt:
                self.__jira_password = getpass.getpass(prompt='Enter Jira Password : ')
            else:
                raise QSTError('Jira Password file is missing.')
        else:
            self.__get_pass()

        self.authorization = (self.jira_user, self.__qsjira_password )    # Name mangling qsjira_password - treated as private
    
    
    def get_test_plan_info_srt(self):
        return
        
    def qst_result_srt(self, testcase_srt, result_srt, comment_srt):
        myTest = synapsert.synapsert()
        self.logging.propagate = False
        
        #
        # Verify test case exists
        #
                        
        try:
            resp, respj = myTest.get_test_cases(self.jira_url,self.authorization,self.test_info_dict['test_plan_key'], self.cert_file)
        except:    #  If the authorization fails the function will fail
            if self.qt_log: self.logging.warning("Function qst_result_srt> INVALID USERNAME -> "+self.test_info_dict['username'])
            sys.exit()
            
        if resp.status_code == 200:     # This means the Test Plan was found
            
            # Verify the Test Case exists 
            testCase_exists = False
            for theTestCases in respj:
                if theTestCases['testCaseKey'] == testcase_srt:
                    testCase_exists = True
                
            if testCase_exists:
                if self.qt_log: self.logging.info("> Test Case Key : "+testcase_srt)
            else:
                if self.qt_log: self.logging.warning("> Test Case Key-> "+ testcase_srt + " <- NOT FOUND")
                sys.exit()

            
        else:   #  Test plan was not found.  Log and exit
            
            if self.qt_log: self.logging.warning("> ERROR with Test Plan "+self.test_info_dict['test_plan_key'])
            sys.exit()
        
        #
        # Verify proper test result given
        #
        
        result_set = ["Passed","Failed","Blocked","Not Tested","NA"]
        
        if result_srt in result_set:
        
            test_run_data = { "testcaseKey":testcase_srt, "result":result_srt,  "comment":comment_srt }
            resp = myTest.update_test_run(self.jira_url, self.authorization, self.test_info_dict['test_plan_key'], self.test_info_dict['testCycleName'], test_run_data, self.cert_file)
            if self.qt_log: self.logging.info("Result: "+result_srt+" > Comment: "+comment_srt)
            if self.qt_log: self.logging.info("-----------------------------")
            
        else:    # Invalid Result Entered
        
            if self.qt_log: self.logging.warning("> INVALID Result Entered -> "+result_srt+" for Test Case Key: "+testcase_srt)
            sys.exit()

        return resp
        
    def qst_test_srt(self,testcase_srt,expected_val,actual_val,msg_pass,msg_fail):
        myTest = synapsert.synapsert()
        self.logging.propagate = False
        #
        # Verify test case exists
        #
                        
        try:
            resp, respj = myTest.get_test_cases(self.jira_url,self.authorization,self.test_info_dict['test_plan_key'], self.cert_file)
        except:    #  If the authorization fails the function will fail
            if self.qt_log: self.logging.warning("Function qst_test_srt> INVALID USERNAME -> "+self.test_info_dict['username'])
            sys.exit()
            
        if resp.status_code == 200:     # This means the Test Plan was found
            
            # Verify the Test Case exists 
            testCase_exists = False
            for theTestCases in respj:
                if theTestCases['testCaseKey'] == testcase_srt:
                    testCase_exists = True
                
            if testCase_exists:
                if self.qt_log: self.logging.info("> Test Case Key : "+testcase_srt)
            else:
                if self.qt_log: self.logging.warning("> Test Case Key-> "+ testcase_srt + " <- NOT FOUND")
                sys.exit()
            
        else:   #  Test plan was not found.  Log and exit
            
            if self.qt_log: self.logging.warning("> ERROR with Test Plan "+self.test_info_dict['test_plan_key'])
            sys.exit()
        
        
        #
        # Upload the log file to Jira/SynapstRT
        # 
        jsonE = json.dumps(expected_val, sort_keys=True)
        jsonA = json.dumps(actual_val, sort_keys=True)

        if jsonE == jsonA:
        
            test_run_data = { "testcaseKey":testcase_srt, "result": 'Passed',  "comment": msg_pass }
            resp = myTest.update_test_run(self.jira_url, self.authorization, self.test_info_dict['test_plan_key'], self.test_info_dict['testCycleName'], test_run_data, self.cert_file)
            if self.qt_log: self.logging.info("Result: Passed...Comment: "+msg_pass)
            if self.qt_log: self.logging.info("-----------------------------")
            
        else:    # jsonA does not equal jsonE, test failed
        
            test_run_data = { "testcaseKey":testcase_srt, "result": 'Failed',  "comment": msg_fail + ' Actual: '+jsonA+ ';  Expected: '+jsonE }
            resp = myTest.update_test_run(self.jira_url, self.authorization, self.test_info_dict['test_plan_key'], self.test_info_dict['testCycleName'], test_run_data, self.cert_file)
            if self.qt_log: self.logging.info("Result: Failed...Comment: "+ msg_fail + " -> Actual: " + jsonA + ";  Expected: " + jsonE)
            if self.qt_log: self.logging.info("-----------------------------")

        return resp
        
    def qst_store_log_srt(self,testcase_srt,logpathname_srt):
        myTest = synapsert.synapsert()
        self.logging.propagate = False
        #
        # Verify allowed to upload file to SynapseRT
        #
        if (self.test_info_dict['allowFileUpload']):
        
            #
            # Verify test case exists
            #
                        
            try:
                resp, respj = myTest.get_test_runs(self.jira_url,self.authorization,self.test_info_dict['test_plan_key'], self.test_info_dict['testCycleName'], self.cert_file)
            except:    #  If the authorization fails the function will fail
                if self.qt_log: self.logging.warning("Function qst_store_log_srt> INVALID USERNAME -> "+self.test_info_dict['username'])
                sys.exit()
            if resp.status_code == 200:     # This means the Test Plan was found
            
            # Verify the Test Case exists and get the test case runID 
                testCase_exists = False
                for theTestCases in respj:
                    if theTestCases['testCaseKey'] == testcase_srt:
                        testCase_exists = True
                        runID = theTestCases['id']
                
                if testCase_exists:
                    if self.qt_log: self.logging.info("> Add Attachment for Test Case Key : "+testcase_srt+"'; Run ID: " +str(runID))
                else:
                    if self.qt_log: self.logging.warning("> Test Case Key-> "+ testcase_srt + " <- NOT FOUND")
                    sys.exit()
            
            else:   #  Test plan was not found.  Log and exit
            
                if self.qt_log: self.logging.warning("> ERROR with Test Plan "+self.test_info_dict['test_plan_key'])
                sys.exit()
            
        #
        #  Upload file to Jira/synapsert
        #
        
            try:
                myTest.add_attachement_test_run(self.jira_url, self.authorization, str(runID), logpathname_srt, self.cert_file)
                if self.qt_log: self.logging.info("> Attachment uploaded for Test Case Key : "+testcase_srt+"'; Run ID: " +str(runID) +"; Attachment: "+ logpathname_srt)
            except:
                if self.qt_log: self.logging.warning("> Error uploading attachment for Test Case Key : "+testcase_srt+"'; Run ID: " +str(runID) +"; Attachment: "+ logpathname_srt)
                sys.exit()
            
        else:
            if self.qt_log: self.logging.warning("> UPLOAD FILE SET TO FALSE. File '"+logpathname_srt+"' Cannot be uploaded to SynapseRT")
        return
    
    def add_attachement_test_run(self, host_url, authorization, runID, file_path_info):
        return
        
    def qst_result(self, testcase, result, comment):
        self.logging.propagate = False

        #
        # select function based on environment data
        #
        
        if self.qt_synapsert:
            qst_result_srt(testcase,result,comment)
            
    def qst_get_test_case_set_srt(self, test_plan_id, cycle_id):
        myTest = synapsert.synapsert()
        self.logging.propagate = False
        

        #
        #  Remove old file containing old list of files
        #
    
        if os.path.exists(self.qst_home+'config/test_case_list.json'):
            os.remove(self.qst_home+'config/test_case_list.json')
        
        if cycle_id and test_plan_id:
        
        #   Get the set of test cases for a given test cycle ID
        #
        
            try:
                resp, respj = myTest.get_test_runs_by_id(self.jira_url,self.authorization, test_plan_id, cycle_id, self.cert_file)
            except:    #  If the authorization fails the function will fail
                if self.qt_log: self.logging.warning("Function qst_test_srt> INVALID USERNAME -> "+self.test_info_dict['username'])
                sys.exit()            

            if resp.status_code == 200:     # This means the Test Plan was found
                testCaseList = []
                if respj:
                    for thesummary in respj:
                        testCaseList.append(thesummary['testCaseKey'])
                else:
                    if self.qt_log: self.logging.info("> QS_TEST, GET TEST CASES: Notice - There are no test cases for the given Test Plan ID "+test_plan_id+" and Test Cycle ID "+cycle_id)
                
                with open(self.qst_home+'config/test_case_list.json', 'w') as json_file:
                    json.dump(testCaseList, json_file)     
                
                if self.qt_log: self.logging.info("* QS_TEST: Test Cases captured for the Test Plan: "+test_plan_id+" and Test Cycle Key: "+cycle_id)
            else:   #  Test plan was not found.  Log and exit
        
                if self.qt_log: self.logging.warning("> QS_TEST, GET TEST CASES: ERROR from getting Test Case for the Test Plan ID "+ test_plan_id +" and its Test Cycles -> "+str(resp.status_code))
                sys.exit()   
                
        elif (not cycle_id and test_plan_id):
                if self.qt_log: self.logging.warning("> QS_TEST, GET TEST CASES: ERROR from getting Test Case - Need both Test Plan ID and Test Cyle ID, only Test Plan ID Given")
                sys.exit()   

        elif (cycle_id and not test_plan_id):
                if self.qt_log: self.logging.warning("> QS_TEST, GET TEST CASES: ERROR from getting Test Case - Need both Test Plan ID and Test Cyle ID, only Test Cycle ID Given")
                sys.exit()   

        else:
        
        #
        #    Get the set of test cases for a given test plan from the user qs_default.py file
        
            try:
                resp, respj = myTest.get_test_cases(self.jira_url,self.authorization,self.test_info_dict['test_plan_key'], self.cert_file)
            except:    #  If the authorization fails the function will fail
                if self.qt_log: self.logging.warning("Function qst_test_srt> INVALID USERNAME -> "+self.test_info_dict['username'])
                sys.exit()
            
            if resp.status_code == 200:     # This means the Test Plan was found
                testCaseList = []
                for thesummary in respj:
                    testCaseList.append(thesummary['testCaseKey'])
                
    
                with open(self.qst_home+'config/test_case_list.json', 'w') as json_file:
                    json.dump(testCaseList, json_file)     
                
                if self.qt_log: self.logging.info("* QS_TEST: Test Cases captured for the Test Plan: "+self.test_info_dict['test_plan_key'])
            else:   #  Test plan was not found.  Log and exit
        
                if self.qt_log: self.logging.warning("> QS_TEST, GET TEST CASES: ERROR from getting Test Case for the given Test Plan ID "+ self.test_info_dict['test_plan_key']+" and its Test Cycles -> "+str(resp.status_code))
                sys.exit()               
        
        return self.test_info_dict['test_plan_key']


if __name__ == '__main__':

    myMainTest = qs_test()
    

