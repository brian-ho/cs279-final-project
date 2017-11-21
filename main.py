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
            "hit_id": "dummy_hitId2",
            "assignment_id": "dummy_assignmentId2",
            "worker_id": "dummy_workerId2",
            "trial": 0,
            "gen": 0,
            "trial_info": trials[0],
            "description": 'This is a test',
            "gmaps_url": GMAPS_URL
            }

        '''
        render_data = {
            "worker_id": request.args.get("workerId"),
            "assignment_id": request.args.get("assignmentId"),
            "amazon_host": AMAZON_HOST,
            "hit_id": request.args.get("hitId"),
            "trial": trials[0],
            "description": 'This is a test',
            "gmaps_url": GMAPS_URL
            }
        '''
        log_task_init(render_data, 'find')

        # Check status
        #query = "SELECT name, type FROM streets WHERE id = %i" % (best_result["street"])
        #cursor.execute(query)
        #street = cursor.fetchone()

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

        query = "SELECT pitch, heading, find_id FROM find WHERE trial = %(trial_)s AND gen = %(gen_)s ORDER BY time DESC;"
        cursor.execute(query, {'trial_':0, 'gen_':0})
        conn.commit()

        imgs = cursor.fetchmany(4)
        print imgs

        render_data = {
            "amazon_host": AMAZON_HOST,
            "hit_id": "dummy_hitId2",
            "assignment_id": "dummy_assignmentId2",
            "worker_id": "dummy_workerId2",
            "trial": 0,
            "gen": 0,
            "trial_info": trials[0],
            "description": 'This is a test',
            "img0": imgs[0],
            "img1": imgs[1],
            "img2": imgs[2],
            "img3": imgs[3]
            }
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
        '''

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
        print "RANKING"
        render_data = {
            "worker_id": "dummy_workerId2",
            "assignment_id": "dummy_assignmentId2",
            "amazon_host": AMAZON_HOST,
            "hit_id": "dummy_hitId2",
            "trial": trials[0],
            "gmaps_key": GMAPS_KEY
            }
        '''
        render_data = {
            "worker_id": request.args.get("workerId"),
            "assignment_id": request.args.get("assignmentId"),
            "amazon_host": AMAZON_HOST,
            "hit_id": request.args.get("hitId"),
            "some_info_to_pass": request.args.get("someInfoToPass")
        }
        '''

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

        query = "INSERT INTO find (hit_id, assignment_id, worker_id, original, updated, time, pitch, heading, trial, gen) VALUES (%(hitId_)s, %(assignmentId_)s, %(workerId_)s, %(original_)s, %(updated_)s, %(time_)s, %(pitch_)s, %(heading_)s, %(trial_)s, %(gen_)s);"
        cursor.execute(query, {
            'hitId_': request.form['hitId'],
            'assignmentId_': request.form['assignmentId'],
            'workerId_': request.form['workerId'],
            'original_': request.form['original'],
            'updated_': request.form['updated'],
            'time_': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'),
            'pitch_': request.form['pitch'],
            'heading_': request.form['heading'],
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
            else:
                v.append(0)
        print v

        query = "INSERT INTO verify (hit_id, assignment_id, worker_id, time, trial, gen, img0, img1, img2, img3, v0, v1, v2, v3) VALUES (%(hitId_)s, %(assignmentId_)s, %(workerId_)s, %(time_)s, %(trial_)s, %(gen_)s, %(img0_)s, %(img1_)s, %(img2_)s, %(img3_)s, %(v0_)s, %(v1_)s, %(v2_)s, %(v3_)s);"
        cursor.execute(query, {
            'hitId_': request.form['hitId'],
            'assignmentId_': request.form['assignmentId'],
            'workerId_': request.form['workerId'],
            'time_': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'),
            'trial_': request.form['trial'],
            'gen_': request.form['gen'],
            'img0_': request.form['img0'],
            'img1_': request.form['img1'],
            'img2_': request.form['img2'],
            'img3_': request.form['img3'],
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

if __name__ == "__main__":
    # app.debug = DEBUG
    app.run(threaded=True)
