import json
import os

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
if 'APP_SETTINGS' in os.environ:
    app.config.from_object(os.environ['APP_SETTINGS'])
else:
    app.config.from_object("config.DevelopmentConfig")
db = SQLAlchemy(app)

from model import *


@app.route('/')
def fetch_stats():
    snapshot = db.session.query(SnapShot).order_by(SnapShot.time).first()
    if snapshot:
        return render_template("snapshot.html", snapshot=snapshot)
    else:
        return render_template("waiting.html")


@app.route('/set/', methods=['POST'])
def set_stats():
    payload = json.loads(request.form['payload'])
    d = payload
    friend_pos = "({0}, {1})".format(d['friend'][0], d['friend'][1])
    enemy_att_pos = "({0}, {1})".format(d['enemy_att'][0], d['enemy_att'][1])
    enemy_def_pos = "({0}, {1})".format(d['enemy_def'][0], d['enemy_def'][1])
    my_pos = "({0}, {1})".format(d['my_pos'][0], d['my_pos'][1])

    snapshot = SnapShot(d['current_zone'], d['dist_to_ball'], d['angle_to_ball'], d['current_state'], d['action'],
                        d['action_duration'], d['is_attacker'], d['in_beam'], d['ball_zone'], d['state_trace'][0],
                        d['action_info'], d['is_ball_close'], d['action_trace'][0], friend_pos, d['friend_zone'],
                        enemy_att_pos, d['enemy_att_zone'], enemy_def_pos, d['enemy_def_zone'], my_pos)
    db.session.add(snapshot)
    db.session.commit()
    return "", 200

if __name__ == '__main__':
    app.run(debug=True)