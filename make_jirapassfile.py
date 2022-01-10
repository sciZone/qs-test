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


import os
import csv
import sys
import json
import shlex
import getpass
import logging
import requests
from cryptography.fernet import Fernet
import base64

# This Application is to be used to generate the Jira password token file 
#  and the supporting key file with the token.
#  This file is read by the QuickSAT Environment to gain secure access 
#  to the Jira Environment
#  
#  Note, this is separate from the Jira Oauth Token Password Setup.  This process
#  is unique to the QuickSAT environment


#
#
# function write_fernet:  This function writes the jira_pw_key and token to the jirapassfile
#
#           jirapassword = the user entered password for the Jira Environment
#
#

def write_fernet(jira_password):
    f = open(f"config/.qsjira_key", "wb")
    password_key = Fernet.generate_key()
    f.write(password_key)
    logging.info('Key generated and written to .qsjira_key')
    f.close()
    
    f = open(f"config/.qsjirapassfile", "wb")
    cipher = Fernet(password_key)
    
    # encode('uft-8') method is used to convert the pgpassword string into a bytes array
    jirapassword_encoded = jira_password.encode('utf-8')
    token = cipher.encrypt(jirapassword_encoded)
    logging.info('Token Generated and written to .qsjirapassfile')
    f.write(token)
    f.close()
    
    return




def main():

    # Enter the pgpassword 
    jirapassword = getpass.getpass('Please enter Jira Password : ')

    try:
        save_jirapassword = write_fernet(jirapassword)
    except Exception as e:
        logging.error(f'Exception - {e}')
        raise

    logging.info('Jira Password token saved')




if __name__ == '__main__':

    # Log all but "debug" messages to the make_pgoassfile.log file
    logging.basicConfig(filename='make_jirapassfile.log',level=logging.INFO)

    # Operate password encryption function
    main()
