import json

from flask import Flask, render_template, request

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
    print payload.keys()
    d = payload
    db_session.add(
        SnapShot(d['current_zone'], d['dist_to_ball'], d['angle_to_ball'], d['current_state'], d['action'],
                 d['action_duration'], d['is_attacker'], d['in_beam'], d['ball_zone'], d['state_trace'],
                 d['action_info'], d['is_ball_close'], d['action_trace'], d['friend'], d['friend_zone'], d['enemy_att'],
                 d['enemy_att_zone'], d['enemy_def'], d['enemy_def_zone'], d['my_pos']))
    return "", 200


@app.route('/synth')
def synth():
    database.init_db()
    print("database initialised")
    return "", 200
