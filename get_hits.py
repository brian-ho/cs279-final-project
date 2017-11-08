import os
#import setup
from flask import Flask, render_template, url_for, request, make_response
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, NumberHitsApprovedRequirement
from boto.mturk.price import Price

#Start Configuration Variables
AWS_ACCESS_KEY_ID = XXX
AWS_SECRET_ACCESS_KEY = XXX
DEV_ENVIROMENT_BOOLEAN = True
DEBUG = True
#End Configuration Variables

#This allows us to specify whether we are pushing to the sandbox or live site.
if DEV_ENVIROMENT_BOOLEAN:
    AMAZON_HOST = "mechanicalturk.sandbox.amazonaws.com"
else:
    AMAZON_HOST = "mechanicalturk.amazonaws.com"

connection = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             host=AMAZON_HOST)

results = connection.get_assignments("3MJ28H2Y1E9P3WEC0KS8V4UACULO57")
print results[0].answers[0][0].fields
