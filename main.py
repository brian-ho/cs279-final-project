#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import psycopg2
import urlparse
from flask import Flask, render_template, url_for, request, make_response
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, NumberHitsApprovedRequirement
from boto.mturk.price import Price
import datetime
import math

# CONFIG VARIABLES
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
GMAPS_KEY = os.environ['GMAPS_KEY']
GMAPS_URL = "https://maps.googleapis.com/maps/api/js?key="+GMAPS_KEY+"&callback=initialize"

DEV_ENVIROMENT_BOOLEAN = True
DEBUG = True

# CONNECTING TO POSTGRES
conn_string = "host='localhost' dbname='cs279' user='brianho' password=''"
print "Connecting to database ...\n	-> %s" % (conn_string)
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

# This allows us to specify whether we are pushing to the sandbox or live site.
if DEV_ENVIROMENT_BOOLEAN:
    AMAZON_HOST = "https://workersandbox.mturk.com/mturk/externalSubmit"
else:
    AMAZON_HOST = "https://www.mturk.com/mturk/externalSubmit"

app = Flask(__name__, static_url_path='')

# ROUTE FOR INTERNAL NAVIGATION
@app.route('/')
def main():
    return render_template('home.html')

# ROUTE FOR FIND TASK
@app.route('/find', methods=['GET', 'POST'])
def find():

    # The following code segment can be used to check if the turker has accepted the task yet
    if request.args.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        # Our worker hasn't accepted the HIT (task) yet
        # TODO RENDER THE CONSENT FORM TEMPLATE
        pass
    else:
        # Our worker accepted the task
        print "FINDING"

        render_data = {
            "amazon_host": AMAZON_HOST,
            "hit_id": "dummy_hitId2", #request.args.get("hitId"),
            "assignment_id": "dummy_assignment_id", #request.args.get("assignmentId"),
            "worker_id": "dummy_workerId2", #request.args.get("workerId"),
            "trial": 0,
            "gen": 0,
            "trial_info": trials[0],
            "description": 'This is a test',
            "gmaps_url": GMAPS_URL
            }

        log_task_init(render_data, 'find')

        resp = make_response(render_template("find.html", name = render_data))

        #This is particularly nasty gotcha.
        #Without this header, your iFrame will not render in Amazon
        resp.headers['x-frame-options'] = 'this_can_be_anything'
        return resp
    return

# ROUTE FOR VERIFY TASK
@app.route('/verify', methods=['GET', 'POST'])
def verify():
#The following code segment can be used to check if the turker has accepted the task yet
    if request.args.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        # Our worker hasn't accepted the HIT (task) yet
        # TODO RENDER THE CONSENT FORM TEMPLATE
        pass
    else:
        #Our worker accepted the task
        print "VERIFYING"

        query = "SELECT pitch, heading, zoom, find_id FROM find WHERE trial = %(trial_)s AND gen = %(gen_)s ORDER BY time DESC;"
        cursor.execute(query, {'trial_':0, 'gen_':0})
        conn.commit()

        results = cursor.fetchmany(4)
        imgs = []

        for i, result in enumerate(results):
            imgs.append([result[0],result[1],zoom_to_FOV(result[2]),result[3]])

        print imgs

        render_data = {
            "amazon_host": AMAZON_HOST,
            "hit_id": "dummy_hitId2", #request.args.get("hitId"),
            "assignment_id" : "dummy_assignment_id", #request.args.get("assignmentId"),
            "worker_id": "dummy_workerId2", #request.args.get("workerId"),
            "trial": 0,
            "gen": 0,
            "trial_info": trials[0],
            "description": 'This is a test',
            "img0": imgs[0],
            "img1": imgs[1],
            "img2": imgs[2],
            "img3": imgs[3]
            }

        log_task_init(render_data, 'verify')

        resp = make_response(render_template("verify.html", name = render_data))
        #This is particularly nasty gotcha.
        #Without this header, your iFrame will not render in Amazon
        resp.headers['x-frame-options'] = 'this_can_be_anything'
        return resp
    return

# ROUTE FOR RANK TASK
@app.route('/rank')#, methods=['GET', 'POST'])
def rank():
#The following code segment can be used to check if the turker has accepted the task yet
    if request.args.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        #Our worker hasn't accepted the HIT (task) yet
        pass
    else:
        #Our worker accepted the task
        query = "SELECT original, updated FROM find WHERE trial = %(trial_)s AND gen = %(gen_)s ORDER BY time DESC;"
        cursor.execute(query, {'trial_':0, 'gen_':0})
        conn.commit()

        results = cursor.fetchmany(4)
        imgs = []

        print "RANKING"
        render_data = {
            "amazon_host": AMAZON_HOST,
            "hit_id": "dummy_hitId2", #request.args.get("hitId"),
            "assignment_id" : "dummy_assignment_id", #request.args.get("assignmentId"),
            "worker_id": "dummy_workerId2", #request.args.get("workerId"),
            "trial": 0,
            "gen": 0,
            "trial_info": trials[0],
            "description": 'This is a test',
            "img0": imgs[0],
            "img1": imgs[1],
            "img2": imgs[2],
            "img3": imgs[3]
            }

        log_task_init(render_data['hit_id'], render_data['assignment_id'], render_data['worker_id'], 'rank')

        resp = make_response(render_template("rank.html", name = render_data))
        #This is particularly nasty gotcha.
        #Without this header, your iFrame will not render in Amazon
        resp.headers['x-frame-options'] = 'this_can_be_anything'
        return resp
    return

# ROUTE FOR SUBMISSION
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    print "SUBMITTED"
    for key,value in request.form.iterlists():
        print key, value

    if request.form['task'] == 'find':
        print "FIND TASK"

        query = "INSERT INTO find (hit_id, assignment_id, worker_id, original, updated, time, pitch, heading, zoom, find_time, trial, gen) VALUES (%(hitId_)s, %(assignmentId_)s, %(workerId_)s, %(original_)s, %(updated_)s, %(time_)s, %(pitch_)s, %(heading_)s, %(zoom_)s, %(findTime_)s, %(trial_)s, %(gen_)s);"
        cursor.execute(query, {
            'hitId_': request.form['hitId'],
            'assignmentId_': request.form['assignmentId'],
            'workerId_': request.form['workerId'],
            'original_': request.form['original'],
            'updated_': request.form['updated'],
            'time_': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'),
            'pitch_': request.form['pitch'],
            'heading_': request.form['heading'],
            'zoom_': request.form['zoom'],
            'findTime_': request.form['findTime'],
            'trial_': request.form['trial'],
            'gen_': request.form['gen']
            })
        conn.commit()

    elif request.form['task'] == 'verify':
        print "VERIFY TASK"

        v = []
        for i in range(4):
            if 'img%i' % i in request.form:
                v.append(1)

                query = "UPDATE find SET valid_count = valid_count + 1 WHERE find_id = %(find_id_)s;"
                cursor.execute(query, {'find_id_': request.form['find_id%i' % i]})
                conn.commit()

            else:
                v.append(0)

                query = "UPDATE find SET invalid_count = invalid_count + 1 WHERE find_id = %(find_id_)s;"
                cursor.execute(query, {'find_id_': request.form['find_id%i' % i]})
                conn.commit()

        print v

        query = "INSERT INTO verify (hit_id, assignment_id, worker_id, time, trial, gen, img0, img1, img2, img3, v0, v1, v2, v3) VALUES (%(hitId_)s, %(assignmentId_)s, %(workerId_)s, %(time_)s, %(trial_)s, %(gen_)s, %(img0_)s, %(img1_)s, %(img2_)s, %(img3_)s, %(v0_)s, %(v1_)s, %(v2_)s, %(v3_)s);"
        cursor.execute(query, {
            'hitId_': request.form['hitId'],
            'assignmentId_': request.form['assignmentId'],
            'workerId_': request.form['workerId'],
            'time_': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'),
            'trial_': request.form['trial'],
            'gen_': request.form['gen'],
            'img0_': request.form['find_id0'],
            'img1_': request.form['find_id1'],
            'img2_': request.form['find_id2'],
            'img3_': request.form['find_id3'],
            'v0_' : v[0],
            'v1_' : v[1],
            'v2_' : v[2],
            'v3_' : v[3]
            })
        conn.commit()


    resp = make_response(render_template("home.html"))
    resp.headers['x-frame-options'] = 'this_can_be_anything'
    return resp

# FUNCTION TO LOG EACH TASK
def log_task_init(render_data, task_):
    # Retrieve relevant data
    hitId_ = render_data['hit_id']
    assignmentId_ = render_data['assignment_id']
    workerId_ = render_data['worker_id']
    trial_ = render_data['trial']
    gen_ = render_data['gen']

    # Log the HIT
    query = "INSERT INTO tracking (hit_id, assignment_id, worker_id, task, status, time, trial, gen) VALUES (%(hitId_)s, %(assignmentId_)s, %(workerId_)s, %(task_)s, 'started', %(time_)s, %(trial_)s, %(gen_)s) RETURNING id;"
    cursor.execute(query, {
        'time_': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'),
        'hitId_': hitId_, 'assignmentId_': assignmentId_,
        'workerId_': workerId_,
        'task_': task_,
        'trial_': trial_,
        'gen_': gen_
        })
    conn.commit()
    print "TRACKING ID", cursor.fetchone()[0]
    return

# HELPER FUNCTION TO CONVER GSV ZOOM TO FOV
def zoom_to_FOV(zoom):
    # Note that we increase zoom by 1
    return math.atan(2**(1 - (zoom+1))) * 360 / math.pi

if __name__ == "__main__":
    # app.debug = DEBUG
    app.run(threaded=True)
