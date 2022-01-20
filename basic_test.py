#!/usr/bin/env python3
"""
Making a basic test case that accepts the test case as a parameter
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

# Fernet is a system for symmetric encryption/decryption

from cryptography.fernet import Fernet

import jira_rest_api
import synapsert

#
#
# function get_fernet:  This function gets the "key" from the key file to decipher the encrypted password
#
#           key_file = the filename storing the key for the file to be decrypted

def get_fernet(key_file):
    with open(f"config/."+key_file, "rb") as f:
        cipher = Fernet(f.read())

    return cipher


#
#
# function parse_args:  This function allows the "config" information and the current QuickSAT information
#                       to be loaded into the QuickSAT Environment
#
#

def parse_args():
    parser = argparse.ArgumentParser(description='Load QuickSAT Data.')
    parser.add_argument('--config',
                        help='Configuration to use.',
                        default='qs_default')


    return parser.parse_args()

def init_logging():
    timestamp = datetime.datetime.now().strftime("Run_%Y_%m_%d_%H_%M_%S")
    logging.basicConfig(filename='log/'+timestamp, encoding='utf-8', level=logging.DEBUG)
    logging.debug('Begin logging')

class qs_test_config():
    def __init__(self, config):
        self.auth_url = config.ENV_CONFIG.get('AUTH_URL', None)
        self.qs_url = config.ENV_CONFIG.get('QS_URL', None)
        self.jira_url = config.ENV_CONFIG.get('JIRA_URL', None)
        self.jira_user = config.ENV_CONFIG.get('JIRA_USER', None)
        self.cert_file = config.ENV_CONFIG.get('CERT_FILE', None)
        self.qt_synapsert = config.ENV_CONFIG.get('QT_SYNAPSERT', False)
        self.qt_log = config.ENV_CONFIG.get('QT_LOG', False)
        self.qt_log_append = config.ENV_CONFIG.get('QT_LOG_APPEND', False)
        self.qs_user = config.ENV_CONFIG.get('QS_USER', None)
        
        qspass_file = config.ENV_CONFIG.get('QS_PASSSFILE', None)
        self.qs_pass_file = ""
        if qspass_file == None:
            self.qs_pass_file = f"config/.qsjirapassfile"
        else:
            self.qs_pass_file = qspass_file

#   
#    Exception Class for qs_test class of functions
#
class QSTError(Exception):
    pass

def init_config():
            #
        #  Get Configuration information
        #
        args = parse_args()              # Define args

        #  Read the configuration information specific to the QuickSAT Environment
        sys.path.append("config")
        #config = __import__(f'config.{args.config}', fromlist=['ENV_CONFIG', 'DATABASE_CONFIG'])
        import qs_emily as config

        result = qs_test_config(config)
        #result = (auth_url, qs_url, jira_url, jira_user, cert_file, qt_synapsert, qt_log, qt_log_append, qs_user, qs_pass_file)
        return result

        
def __get_pass(qt_config):
    # get the token
    key_file = "qsjira_key"
    __cipher = get_fernet(key_file)
        
    # Extract the halo Password from the .qsjira_key
    #    The password must also be decoded from "utf-8"
    with open(qt_config.qs_pass_file, 'rb') as pf:
        __qsjira_password = __cipher.decrypt(pf.read()).decode()
        logging.info("User Password found and extracted")
        return __qsjira_password

def get_token(qt_config):
        if qt_config.auth_url == None:
            raise QSTError('Authentication URL not defined.')

        if qt_config.jira_user == None:
            raise QSTError('Jira User not defined.')

        if not os.path.exists(qt_config.qs_pass_file):
            raise QSTError('Jira Password file is missing.')
        else:
            qsjira_password = __get_pass(qt_config)

        return (qt_config.jira_user, qsjira_password )    # Name mangling qsjira_password - treated as private
    
def main_loop():
    init_logging()
    qt_config = init_config()
    authorization = get_token(qt_config)
    jira = jira_rest_api.jira_rest()
    try:
        url = qt_config.jira_url + '/rest/synapse/latest/public/testPLan' + 'VSMFSW-2267' + '/cycles'
        resp = jira.api_request_get(qt_config.jira_url, authorization)
    except Exception as e:
        print(e)



if __name__ == '__main__':

    main_loop()