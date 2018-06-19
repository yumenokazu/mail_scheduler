from datetime import datetime


class Player():
    base_datetime = datetime(2018, 6, 19, 0, 0, 0)
    idle_time = 12

    def __init__(self, name, offset, duration=None):
        self.name = name
        self.offset = offset    # offset for the first full-time run
        if duration is None:
            self.duration = 18
        else:
            self.duration = duration        # general run duration

    def should_start(self, current_time):
        delta_since_base = current_time - self.base_datetime
        days, seconds = delta_since_base.days, delta_since_base.seconds
        h_since_base = days * 24 + seconds // 3600
        if h_since_base == 0 and self.offset > self.idle_time:
            return True
        if((h_since_base - self.offset) % (self.duration + self.idle_time)) == 0:
            return True
        else:
            return False

    def should_end(self, current_time):
        end_offset = self.offset + self.duration
        delta_since_base = current_time - self.base_datetime
        days, seconds = delta_since_base.days, delta_since_base.seconds
        h_since_base = days * 24 + seconds // 3600
        if ((h_since_base - end_offset) % (self.duration + self.idle_time)) == 0:
            return True
        else:
            return False

    def __repr__(self):
        return "<Player(name=%s)>" % (self.name)


def create_players():
    return [Player('Starzky', offset=0),
            Player('Scrattar', offset=6),
            Player('Hatin', offset=12),
            Player('Sel', offset=18),
            Player('Yume', offset=24)]
            #Player('Dank', offset=18, duration=12),
            #Player('Doge', offset=6, duration=12)]
