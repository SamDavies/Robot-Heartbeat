import datetime

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime

from app.database import Base


class SnapShot(Base):
    __tablename__ = 'snapshot'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    current_zone = Column(String(100))
    dist_to_ball = Column(Integer)
    angle_to_ball = Column(Float)
    current_state = Column(String(100))
    action = Column(String(100))
    action_duration = Column(Float)
    is_attacker = Column(Boolean)
    in_beam = Column(Boolean)
    ball_zone = Column(String(100))
    state_trace = Column(String(100))
    action_info = Column(String(100))
    is_ball_close = Column(Boolean)
    action_trace = Column(String(100))
    friend = Column(String(100))
    friend_zone = Column(Integer)
    enemy_att = Column(String(100))
    enemy_att_zone = Column(Integer)
    enemy_def = Column(String(100))
    enemy_def_zone = Column(Integer)
    my_pos = Column(String(100))

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __init__(self, current_zone, dist_to_ball, angle_to_ball, current_state, action, action_duration, is_attacker,
                 in_beam, ball_zone, state_trace, action_info, is_ball_close, action_trace, friend, friend_zone,
                 enemy_att, enemy_att_zone, enemy_def, enemy_def_zone, my_pos):

        self.time = datetime.datetime.now()
        self.current_zone = current_zone
        self.dist_to_ball = dist_to_ball
        self.angle_to_ball = angle_to_ball
        self.current_state = current_state
        self.action = action
        self.action_duration = action_duration
        self.is_attacker = is_attacker
        self.in_beam = in_beam
        self.ball_zone = ball_zone
        self.state_trace = state_trace
        self.action_info = action_info
        self.is_ball_close = is_ball_close
        self.action_trace = action_trace
        self.friend = friend
        self.friend_zone = friend_zone
        self.enemy_att = enemy_att
        self.enemy_att_zone = enemy_att_zone
        self.enemy_def = enemy_def
        self.enemy_def_zone = enemy_def_zone
        self.my_pos = my_pos

    def __repr__(self):
        return '<Robot - %r>' % (self.id)
