#!/usr/bin/env python3

"""
Test Configuration Entry


Copyright (c) 2021-2022, sci_Zone, Inc.

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

import os
import csv
import sys
import json

#
#  This application is a simple function to store the Test Plan and the 
#    current Test Cycle.  This information is stored in a configuration 
#    file.  This can also be called from a function to start the Jenkins pipeline



def main():

    confirm_enter = 'N'
    confirm_enter_2 = 'N'
    confirm_enter_3 = 'N'
    
    # Enter the Username
    username_notEntered = True
    while username_notEntered:
        username = input('Please enter your username : ') or None
        if username is not None:
            confirm_enter_3 = input('--> CONFIRM Username entered '+username+' [Y] or N: ') or 'Y'
            if confirm_enter_3 == "Y":
                username_notEntered = False
    
    # Enter the Test Plan Key
    testKey_notEntered = True
    while testKey_notEntered:
        test_plan_key = input('Please enter the Test Plan Key : ') or None
        if test_plan_key is not None:
            confirm_enter = input('--> CONFIRM Test Plan Key entered '+test_plan_key+' [Y] or N: ') or 'Y'
            if confirm_enter == "Y":
                testKey_notEntered = False
                
    # Enter the Test Cycle Name 
    testCycleName_notEntered = True
    while testCycleName_notEntered:
        testCycleName = input('Please enter the Test Cycle Name : ') or None
        if testCycleName is not None:
            confirm_enter_2 = input('--> CONFIRM Test Plan Key entered '+testCycleName+' [Y] or N: ') or 'Y'
            if confirm_enter_2 == "Y":
                testCycleName_notEntered = False

    # Enter if operator wants to allow the file upload
    allowFileUpload_notEntered = True
    while allowFileUpload_notEntered:
        allowFileUpload = input('Do you want to allow file uploads to SynapseRT?:  [Y] or N:') or 'Y'
        if allowFileUpload is not None:
            if (allowFileUpload == "Y" or allowFileUpload == "y"):
                allowFileUpload_l = True
                allowFileUpload_notEntered = False
            elif (allowFileUpload == "N" or allowFileUpload == "n"):
                allowFileUpload_l = False
                allowFileUpload_notEntered = False
            else:
                allowFileUpload_notEntered = True

                
    # Save the results in a JSON file
    
    test_execution_info = {"username": username, "test_plan_key": test_plan_key, "testCycleName": testCycleName, "allowFileUpload": allowFileUpload_l }
    with open('config/test_info.json', 'w') as json_file:
        json.dump(test_execution_info, json_file)

if __name__ == '__main__':

    # Operate the capture of the Test Execution information
    main()
