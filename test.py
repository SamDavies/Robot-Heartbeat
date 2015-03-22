import unittest
import os
import tempfile
import json

import app


__author__ = 'Sam Davies'


class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        # Flask-WTForms is trying to validate your CSRF token
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_set(self):
        response = self.add_snapshot()
        raw_json = response.data
        self.assertNotIn(b'Waiting for a heartbeat', raw_json)
        self.assertEquals(response.status_code, 200)

    def add_snapshot(self):
        payload = {'current_zone': '0', 'dist_to_ball': '0',
                    'angle_to_ball': '0', 'current_state': '0', 'action': '0',
                    'action_duration': '0', 'is_attacker': '0', 'in_beam': '0',
                    'ball_zone': '0', 'state_trace': ['0'], 'action_info': '0',
                    'is_ball_close': '0', 'action_trace': ['0'], 'friend': [0, 1],
                    'friend_zone': '0', 'enemy_att': [0, 2], 'enemy_att_zone': '0',
                    'enemy_def': [0, 3], 'enemy_def_zone': '0', 'my_pos': [0, 4]}
        payload_json = json.dumps(payload)
        # check the thing feed
        return self.app.post('/set/', data=dict(payload=payload_json))

    def test_db_limit(self):
        response = self.add_snapshot()
        self.assertEquals(response.data, b'1001')
