#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import psycopg2
from flask import Flask, render_template, url_for, request, make_response
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, NumberHitsApprovedRequirement
from boto.mturk.price import Price

# CONFIG VARIABLES
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
GMAPS_KEY = os.environ['GMAPS_KEY']
GMAPS_URL = "https://maps.googleapis.com/maps/api/js?key="+GMAPS_KEY+"&callback=initialize"

DEV_ENVIROMENT_BOOLEAN = True
DEBUG = True

# CONNECTING TO POSTGRES
conn_string = "host='localhost' dbname='cs279' user='brianho' password=''"
print "Connecting to database\n	-> %s" % (conn_string)
# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)
'''
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
'''
# conn.cursor will return a cursor object, you can use this cursor to perform queries
cursor = conn.cursor()
print "Connected!\n"

# Setup trials
trials = [{
            "lat":42.372835,
            "lng": -71.116921
            },
            {
            "lat":42.375858,
            "lng":-71.114258},
            {
            "lat":42.378687,
            "lng":-71.116619}
            ]

trial_ind = 0
generation = 0
counts = [0,0,0]


# This allows us to specify whether we are pushing to the sandbox or live site.
if DEV_ENVIROMENT_BOOLEAN:
    AMAZON_HOST = "https://workersandbox.mturk.com/mturk/externalSubmit"
else:
    AMAZON_HOST = "https://www.mturk.com/mturk/externalSubmit"

app = Flask(__name__, static_url_path='')

@app.route('/')
def main():
    return render_template('home.html')

# ROUTE FOR FIND TASK
@app.route('/find', methods=['GET', 'POST'])
def find():

# The following code segment can be used to check if the turker has accepted the task yet
    if request.args.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        #Our worker hasn't accepted the HIT (task) yet
        pass
    else:
        #Our worker accepted the task
        print "FIND — current generation is %i" % (generation)
        print "FIND — image %i, count %i" % (trial_ind, counts[trial_ind])

        # Ask database for info


        counts[trial_ind] += 1


        pass

    # SOME LOGIC TO GET THE CURRENT IMAGE

    '''
    We're creating a dict with which we'll render our template page.html
    Note we are grabbing GET Parameters
    In this case, I'm using someInfoToPass as a sample parameter to pass information
    '''
    render_data = {
        "worker_id": request.args.get("workerId"),
        "assignment_id": request.args.get("assignmentId"),
        "amazon_host": AMAZON_HOST,
        "hit_id": request.args.get("hitId"),
        "trial": trials[trial_ind],
        "gmaps_url": GMAPS_URL
        }

    resp = make_response(render_template("find.html", name = render_data))
    #This is particularly nasty gotcha.
    #Without this header, your iFrame will not render in Amazon
    resp.headers['x-frame-options'] = 'this_can_be_anything'
    return resp

# ROUTE FOR VERIFY TASK
@app.route('/verify')#, methods=['GET', 'POST'])
def verify():
#The following code segment can be used to check if the turker has accepted the task yet
    if request.args.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        #Our worker hasn't accepted the HIT (task) yet
        pass
    else:
        #Our worker accepted the task
        pass

    '''
    We're creating a dict with which we'll render our template page.html
    Note we are grabbing GET Parameters
    In this case, I'm using someInfoToPass as a sample parameter to pass information
    '''
    render_data = {
        "worker_id": request.args.get("workerId"),
        "assignment_id": request.args.get("assignmentId"),
        "amazon_host": AMAZON_HOST,
        "hit_id": request.args.get("hitId"),
        "some_info_to_pass": request.args.get("someInfoToPass"),
        "img1": "img1",
        "img2": "img2",
        "img3": "img3",
        "img4": "img4"
    }

    resp = make_response(render_template("verify.html", name = render_data))
    #This is particularly nasty gotcha.
    #Without this header, your iFrame will not render in Amazon
    resp.headers['x-frame-options'] = 'this_can_be_anything'
    return resp

# ROUTE FOR EDIT TASK
@app.route('/edit')#, methods=['GET', 'POST'])
def edit():
#The following code segment can be used to check if the turker has accepted the task yet
    if request.args.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        #Our worker hasn't accepted the HIT (task) yet
        pass
    else:
        #Our worker accepted the task
        pass

    '''
    We're creating a dict with which we'll render our template page.html
    Note we are grabbing GET Parameters
    In this case, I'm using someInfoToPass as a sample parameter to pass information
    '''
    render_data = {
        "worker_id": request.args.get("workerId"),
        "assignment_id": request.args.get("assignmentId"),
        "amazon_host": AMAZON_HOST,
        "hit_id": request.args.get("hitId"),
        "some_info_to_pass": request.args.get("someInfoToPass")
    }

    resp = make_response(render_template("edit.html", name = render_data))
    #This is particularly nasty gotcha.
    #Without this header, your iFrame will not render in Amazon
    resp.headers['x-frame-options'] = 'this_can_be_anything'
    return resp

# ROUTE FOR RANK TASK
@app.route('/rank')#, methods=['GET', 'POST'])
def rank():
#The following code segment can be used to check if the turker has accepted the task yet
    if request.args.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        #Our worker hasn't accepted the HIT (task) yet
        pass
    else:
        #Our worker accepted the task
        pass

    '''
    We're creating a dict with which we'll render our template page.html
    Note we are grabbing GET Parameters
    In this case, I'm using someInfoToPass as a sample parameter to pass information
    '''
    render_data = {
        "worker_id": request.args.get("workerId"),
        "assignment_id": request.args.get("assignmentId"),
        "amazon_host": AMAZON_HOST,
        "hit_id": request.args.get("hitId"),
        "some_info_to_pass": request.args.get("someInfoToPass")
    }

    resp = make_response(render_template("rank.html", name = render_data))
    #This is particularly nasty gotcha.
    #Without this header, your iFrame will not render in Amazon
    resp.headers['x-frame-options'] = 'this_can_be_anything'
    return resp

# ROUTE FOR SUBMISSION
@app.route('/submit', methods=['GET', 'POST'])
def submit():
#The following code segment can be used to check if the turker has accepted the task yet
    if request.args.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        #Our worker hasn't accepted the HIT (task) yet
        pass
    else:
        #Our worker accepted the task
        pass

    print "SUBMITTED"

    '''
    We're creating a dict with which we'll render our template page.html
    Note we are grabbing GET Parameters
    In this case, I'm using someInfoToPass as a sample parameter to pass information
    render_data = {
        "worker_id": request.args.get("workerId"),
        "assignment_id": request.args.get("assignmentId"),
        "amazon_host": AMAZON_HOST,
        "hit_id": request.args.get("hitId"),
        "some_info_to_pass": request.args.get("someInfoToPass")
    }
    '''

    resp = make_response(render_template("home.html"))
    #This is particularly nasty gotcha.
    #Without this header, your iFrame will not render in Amazon
    resp.headers['x-frame-options'] = 'this_can_be_anything'
    return resp


if __name__ == "__main__":
    app.debug = DEBUG
    app.run()
