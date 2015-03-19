import json

from flask import Flask, render_template, request
import requests

from database import db_session
import database
from app.model import SnapShot


app = Flask(__name__)
# Load from file
app.config.from_object('config')


@app.route('/')
def fetch_stats():
    snapshot = db_session.query(SnapShot).order_by(SnapShot.time).first()
    if snapshot:
        return render_template("snapshot.html", snapshot=snapshot)
    else:
        return render_template("waiting.html")


@app.route('/set/', methods=['POST'])
def set_stats():
    payload = json.loads(request.form['payload'])
    d = payload
    snapshot = SnapShot(d['current_zone'], d['dist_to_ball'], d['angle_to_ball'], d['current_state'], d['action'],
                        d['action_duration'], d['is_attacker'], d['in_beam'], d['ball_zone'], d['state_trace'][0],
                        d['action_info'], d['is_ball_close'], d['action_trace'][0], d['friend'], d['friend_zone'], d['enemy_att'],
                        d['enemy_att_zone'], d['enemy_def'], d['enemy_def_zone'], d['my_pos'])
    db_session.add(snapshot)
    db_session.commit()
    return "", 200


@app.route('/synth')
def synth():
    print "initialising"
    database.init_db()
    print "database initialised"
    payload = {'current_zone': '0', 'dist_to_ball': '0',
                    'angle_to_ball': '0', 'current_state': '0', 'action': '0',
                    'action_duration': '0', 'is_attacker': '0', 'in_beam': '0',
                    'ball_zone': '0', 'state_trace': '0', 'action_info': '0',
                    'is_ball_close': '0', 'action_trace': '0', 'friend': '0',
                    'friend_zone': '0', 'enemy_att': '0', 'enemy_att_zone': '0',
                    'enemy_def': '0', 'enemy_def_zone': '0', 'my_pos': '0'}
    payload_json = json.dumps(payload)
    # check the thing feed
    payload = json.loads(payload_json)
    d = payload
    snapshot = SnapShot(d['current_zone'], d['dist_to_ball'], d['angle_to_ball'], d['current_state'], d['action'],
                        d['action_duration'], d['is_attacker'], d['in_beam'], d['ball_zone'], d['state_trace'],
                        d['action_info'], d['is_ball_close'], d['action_trace'], d['friend'], d['friend_zone'], d['enemy_att'],
                        d['enemy_att_zone'], d['enemy_def'], d['enemy_def_zone'], d['my_pos'])
    db_session.add(snapshot)
    db_session.commit()

    return "", 200
