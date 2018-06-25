from datetime import datetime


class Instance:
    base_datetime = datetime(2018, 6, 19, 0, 0, 0)
    idle_time = 12

    def __init__(self, name, offset, duration=None):
        self.name = name
        self.offset = int(offset)    # offset for the first full-time run
        if duration is None:
            self.duration = 18
        else:
            self.duration = int(duration)        # general run duration

    @property
    def full_cycle(self):
        return self.idle_time + self.duration

    def should_start(self, current_time):
        delta_since_base = current_time - self.base_datetime
        days, seconds = delta_since_base.days, delta_since_base.seconds
        h_since_base = days * 24 + seconds // 3600
        if h_since_base == 0 and self.offset > self.idle_time:
            return True
        if((h_since_base - self.offset) % self.full_cycle) == 0:
            return True
        else:
            return False

    def should_end(self, current_time):
        end_offset = self.offset + self.duration
        delta_since_base = current_time - self.base_datetime
        days, seconds = delta_since_base.days, delta_since_base.seconds
        h_since_base = days * 24 + seconds // 3600
        if ((h_since_base - end_offset) % self.full_cycle) == 0:
            return True
        else:
            return False

    def is_running(self, current_time):
        delta_since_base = current_time - self.base_datetime
        days, seconds = delta_since_base.days, delta_since_base.seconds
        h_since_base = days * 24 + seconds // 3600
        remainder = (h_since_base - self.offset) % (self.full_cycle)
        if remainder == 0:
            return True
        elif remainder < self.duration:
            return True
        else:
            return False

    def __repr__(self):
        return "<Instance(name=%s)>" % (self.name)


def create_from_csv(path):
    """
    Read csv file and return list of Instance
    :param path: path to file
    :return: list of Instance
    """
    import csv

    with open(path, newline='') as f:
        reader = csv.reader(f)
        return [Instance(*row) for row in reader]


