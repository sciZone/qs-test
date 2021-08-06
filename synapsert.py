#!/usr/bin/env python3

"""
Core Test Class for SynapseRT Rest API Tool


Copyright (c) 2018-2021, sci_Zone, Inc.

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
import jira_rest_api


class synapsert(object):

    def __init__(self):
        pass

# -----------------------------------------------------------------------------------
#
# Test Plan Resource
#

#
#Test Assignment from Test Plan level
#

#
# Add Test Cycle to Test Plan
#


#
# Get all test cycles for a given test plan
#
    def get_test_cycles(self,host_url, authorization, test_plan_key):
        
            heyJira = jira_rest_api.jira_rest()
            cycles_rest_api = host_url+'/rest/synapse/latest/public/testPlan/'+test_plan_key+'/cycles'
            resp_rest = heyJira.api_request_get(cycles_rest_api, authorization)
            respj = resp_rest.json()

            return resp_rest, respj
            
#
# Get all test cases for a test plan
#
    def get_test_cases(self,host_url, authorization, test_plan_key):
        
            heyJira = jira_rest_api.jira_rest()
            test_plans_rest_api = host_url+'/rest/synapse/latest/public/testPlan/'+test_plan_key+'/members'
            resp_rest = heyJira.api_request_get(test_plans_rest_api, authorization)
            respj = resp_rest.json()

            return resp_rest, respj

#
# Get all test run details for a test plan
#
    def get_run_details_cases(self,host_url, authorization, test_plan_key):
        
            heyJira = jira_rest_api.jira_rest()
            test_run_details_rest_api = host_url+'/rest/synapse/latest/public/testPlan/'+test_plan_key+'/testPlanInformation'
            resp_rest = heyJira.api_request_get(test_run_details_rest_api, authorization)
            respj = resp_rest.json()

            return resp_rest, respj

#
# Get all defects for a test plan
#
    def get_defects_plan(self,host_url, authorization, test_plan_key):
        
            heyJira = jira_rest_api.jira_rest()
            test_plan_defects_rest_api = host_url+'/rest/synapse/latest/public/testPlan/'+test_plan_key+'/defects'
            resp_rest = heyJira.api_request_get(test_plan_defects_rest_api, authorization)
            respj = resp_rest.json()

            return resp_rest, respj

#
# ADD Test Case(s) to Test Plan
#
#    Format (Example):
#
#	{
#		"testCaseKeys":["FRS-1","FRS-2","FRS-3"]
#	}


    def post_test_to_plan(self,host_url, authorization, test_plan_key, data_api):
        
            heyJira = jira_rest_api.jira_rest()
            test_to_plan_rest_api = host_url+'/rest/synapse/latest/public/testPlan/'+test_plan_key+'/addMembers'
            resp_rest = heyJira.api_request_post(test_to_plan_rest_api, data_api, authorization)

            return resp_rest


# -----------------------------------------------------------------------------------
#
# Test Cycle Resource
#

#
#	Test Assignment from Test Cycle level
#


#
# Update Test Cycle  
#
#  Valid actions are:
#		- Start
#		- Complete
#		- Abort
#		- Resume
#
#
    def update_test_cycle(self,host_url, authorization, test_plan_key, cycleName, action):
        
            heyJira = jira_rest_api.jira_rest()
            test_cycle_update_rest_api = host_url+'/rest/synapse/latest/public/testPlan/'+test_plan_key+'/cycle/'+cycleName+'/wf/'+action
            data_api = {}
            resp_rest = heyJira.api_request_put(test_cycle_update_rest_api, data_api, authorization)

            return resp_rest
            
#
# Update Test Cycle Details
#
#
#    Format (example):
#
#   {
#	 "id": 152,
#	 "name":"Round 2 with Firefox_Update",
#	  "environment":"Firefox 47_Update",
#	  "build":"8.4_Update",
#	  "plannedStartDate":"2017-04-13",
#	  "plannedEndDate":"2017-04-15"
#	}
#

    def update_test_cycle_details(self,host_url, authorization, test_plan_key, test_cycle_details):
        
            heyJira = jira_rest_api.jira_rest()
            test_cycle_update_details_rest_api = host_url+'/rest/synapse/latest/public/testPlan/'+test_plan_key+'/editCycle/'
            resp_rest = heyJira.api_request_post(test_cycle_update_details_rest_api, test_cycle_details, authorization)

            return resp_rest


#
#     Get Test Runs in a test cycle
#

    def get_test_runs(self,host_url, authorization, test_plan_key, cycleName):
        
            heyJira = jira_rest_api.jira_rest()
            test_runs_cycle_rest_api = host_url+'/rest/synapse/latest/public/testPlan/'+test_plan_key+'/cycle/'+cycleName+'/testRuns'
            resp_rest = heyJira.api_request_get(test_runs_cycle_rest_api, authorization)
            respj = resp_rest.json()

            return resp_rest, respj


#
#     Get Test Runs in a test cycle by Cycle ID
#

    def get_test_runs_by_id(self,host_url, authorization, test_plan_key, cycleId):
        
            heyJira = jira_rest_api.jira_rest()
            test_runs_cycle_id_rest_api = host_url+'/rest/synapse/latest/public/testPlan/'+test_plan_key+'/cycle/'+cycleId+'/testRunsByCycleId'
            resp_rest = heyJira.api_request_get(test_runs_cycle_id_rest_api, authorization)
            respj = resp_rest.json()

            return resp_rest, respj
            
#
#     Add/Remove Test Cases from Test Cycle
#

#
#     Re-Order Test Runs in a Test Cycle
#


#
#     Get Defects from a Test Cycle
#

    def get_cycle_defects_by_id(self,host_url, authorization, test_plan_key, cycleId):
        
            heyJira = jira_rest_api.jira_rest()
            defects_cycle_id_rest_api = host_url+'/rest/synapse/latest/public/testPlan/'+test_plan_key+'/cycle/'+cycleId+'/defects'
            resp_rest = heyJira.api_request_get(defects_cycle_id_rest_api, authorization)
            respj = resp_rest.json()

            return resp_rest, respj


# -----------------------------------------------------------------------------------
#
# Test Run Resource
#

#
#	Get Test Run Details
#
    def get_test_run_details(self,host_url, authorization, run_id):
            heyJira = jira_rest_api.jira_rest()
            test_run_res_rest_api = host_url+'/rest/synapse/latest/public/testRun/'+run_id
            resp_rest = heyJira.api_request_get(test_run_res_rest_api, authorization)
            respj = resp_rest.json()

            return resp_rest, respj


#
# Update Test Run 
#
#   Format (example)
#  {
#		"testcaseKey":"FRS-14",
#		"result":"Passed",
#		"comment":"Updated through REST"
#  }
#
#  Valid Results: Passed, Failed, Blocked, Not Tested, NA

    def update_test_run(self,host_url, authorization, test_plan_key, cycleName, test_run_data):
        
            heyJira = jira_rest_api.jira_rest()
            test_run_update_rest_api = host_url+'/rest/synapse/latest/public/testPlan/'+test_plan_key+'/cycle/'+cycleName+'/updateTestRun'
            resp_rest = heyJira.api_request_post(test_run_update_rest_api, test_run_data, authorization)

            return resp_rest

#
# Update Test Run Step Result
#
#   Format (example)
# { 
#  "runStepId":15366, "result":"Blocked", "actualResult":"This Test Step is failed.", "bugs":["FRS-23"]
# }


    def update_test_run_step(self,host_url, authorization, runID, test_run_data):
        
            heyJira = jira_rest_api.jira_rest()
            test_run_update__step_rest_api = host_url+'/rest/synapse/latest/public/testRun/updateStep/'+runID
            resp_rest = heyJira.api_request_post(test_run_update__step_rest_api, test_run_data, authorization)

            return resp_rest



#
# Update Test Run Result with runid
#
#   Format (example)
# {
# 	"runId":"3174", "result":"Failed", "comment":"Updated through REST API", "bugs":["FRS-24"]
# }

    def update_test_run_results(self, host_url, authorization, test_run_data):
   
            heyJira = jira_rest_api.jira_rest()
            test_run_results_update_rest_api = host_url+'/rest/synapse/latest/public/testRun/update'
            resp_rest = heyJira.api_request_post(test_run_results_update_rest_api, test_run_data, authorization)

            return resp_rest
         
#            
#   Add Attachments to Test Run
#

    def add_attachement_test_run(self, host_url, authorization, runID, file_path_info):
   
            heyJira = jira_rest_api.jira_rest()
            test_run_results_update_rest_api = host_url+'/rest/synapse/latest/public/attachment/'+runID+'/testrun'
            resp_rest = heyJira.api_request_post_upload_file(test_run_results_update_rest_api, file_path_info, authorization)

            return resp_rest
 
#
#    Get Attachment Details from a Test Run
#

    def get_attachment_details_test_run(self,host_url, authorization, run_id):
            heyJira = jira_rest_api.jira_rest()
            test_run_attachement_details_api = host_url+'/rest/synapse/latest/public/attachment/'+run_id+'/getAttachmentDetails'
            resp_rest = heyJira.api_request_get(test_run_attachement_details_api, authorization)
            respj = resp_rest.json()

            return resp_rest, respj

#
# Delete Attachment from a Test Run
#

    def delete_attachement_TestRun(self,host_url, authorization, runID, attachmentID):
            heyJira = jira_rest_api.jira_rest()
            delete_attachement_runId_rest_api = host_url+'/rest/synapse/latest/public/attachment/'+runID+'/deleteAttachment/'+attachmentID
            resp_rest = heyJira.api_request_delete(delete_attachement_runId_rest_api, '{}', authorization)

            return resp_rest

# -----------------------------------------------------------------------------------
#
# Test Case Resource
#


#
# Add Test Steps to a Test Case
#
#
# [
#  { "step":"Step 1 added via REST API",
#     "stepData": "It is step data A for testing",
#     "expectedResult":"Expected Result 1 added via REST API" 
#   },
#   {   "step":"Step 2 added via REST API", 
#    "stepData": "It is step data B for testing", 
#    "expectedResult":"Expected Result 1 added via REST API" 
#   }
#  ]

    def add_test_case_step_results(self, host_url, authorization, testCaseIssueKey, test_case_step_data):
   
            heyJira = jira_rest_api.jira_rest()
            test_case_add_step_rest_api = host_url+'/rest/synapse/latest/public/testCase/'+testCaseIssueKey+'/addSteps'
            resp_rest = heyJira.api_request_post(test_case_add_step_rest_api, test_case_step_data, authorization)

            return resp_rest
            
#
#	Get Test Steps from a Test Case
#
    def get_steps_test_case(self,host_url, authorization, testCaseIssueKey):
            heyJira = jira_rest_api.jira_rest()
            get_test_case_steps_rest_api = host_url+'/rest/synapse/latest/public/testCase/'+testCaseIssueKey+'/steps'
            resp_rest = heyJira.api_request_get(get_test_case_steps_rest_api, authorization)
            respj = resp_rest.json()

            return resp_rest, respj
            
            
#
#  Delete Test Step from Test Case with ID
#


    def delete_step_by_id(self,host_url, authorization, testCaseIssueKey, stepID):
            heyJira = jira_rest_api.jira_rest()
            delete_step_by_id_rest_api = host_url+'/rest/synapse/latest/public/testCase/'+testCaseIssueKey+'/deleteStep/'+stepID
            resp_rest = heyJira.api_request_delete(delete_step_by_id_rest_api, '{}', authorization)

            return resp_rest
            
            
            
#            
#  Delete Test Step from Test Case with sequenceNumber
#

    def delete_step_by_No(self,host_url, authorization, testCaseIssueKey, stepNo):
            heyJira = jira_rest_api.jira_rest()
            delete_step_by_stepNo_rest_api = host_url+'/rest/synapse/latest/public/testCase/'+testCaseIssueKey+'/deleteStepBySequenceNo/'+stepNo
            resp_rest = heyJira.api_request_delete(delete_step_by_stepNo_rest_api, '{}', authorization)

            return resp_rest