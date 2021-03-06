import json
import os

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import time
from sqlalchemy.orm import aliased


app = Flask(__name__)
if 'APP_SETTINGS' in os.environ:
    app.config.from_object(os.environ['APP_SETTINGS'])
else:
    app.config.from_object("config.DevelopmentConfig")
db = SQLAlchemy(app)

from model import *


@app.route('/')
def fetch_stats():
    return render_template("snapshot.html")

@app.route('/refresh')
def refresh_stats():
    snapshot = db.session.query(SnapShot).order_by(SnapShot.time.desc()).first()
    time_dif = (datetime.datetime.now() - snapshot.time)
    time_print = "{0}.{1}".format(time_dif.seconds, int(time_dif.microseconds/10000))
    if snapshot:
        return render_template("snapshot_data.html", snapshot=snapshot, time=time_print)
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

    # add the new snapshot
    db.session.add(snapshot)

    # keep the number of snapshots below 5000
    rows = db.session.query(SnapShot).count()

    if rows > 1000:

        # get the time of the 5000th row
        snapshots_1 = aliased(SnapShot, name="S1")

        top_snapshots = db.session.query(snapshots_1.id).order_by(snapshots_1.time.desc()).limit(1000).subquery()
        SnapShot.query.filter(~SnapShot.id.in_(top_snapshots)).delete(synchronize_session='fetch')

    db.session.commit()

    return str(rows), 200

if __name__ == '__main__':
    app.run(debug=True)