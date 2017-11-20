import os
import sys
#import setup
from flask import Flask, render_template, url_for, request, make_response
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, NumberHitsApprovedRequirement
from boto.mturk.price import Price

#Start Configuration Variables
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
DEV_ENVIROMENT_BOOLEAN = True
DEBUG = True
#End Configuration Variables

AWS_id = sys.argv[1]

#This allows us to specify whether we are pushing to the sandbox or live site.
if DEV_ENVIROMENT_BOOLEAN:
    AMAZON_HOST = "mechanicalturk.sandbox.amazonaws.com"
else:
    AMAZON_HOST = "mechanicalturk.amazonaws.com"

connection = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             host=AMAZON_HOST)

results = connection.get_assignments(AWS_id)
assignment = results[0]
# print results[0].WorkerId
for answer in assignment.answers[0]:
    print answer.qid, answer.fields[0]
