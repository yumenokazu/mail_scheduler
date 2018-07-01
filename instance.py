from jsonschema import ValidationError

from app import app


class Instance:
    base_datetime = app.config.get("INSTANCE_START_DATE")
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
        delta_since_base = current_time - Instance.base_datetime
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
        delta_since_base = current_time - Instance.base_datetime
        days, seconds = delta_since_base.days, delta_since_base.seconds
        h_since_base = days * 24 + seconds // 3600
        if ((h_since_base - end_offset) % self.full_cycle) == 0:
            return True
        else:
            return False

    def is_running(self, current_time):
        delta_since_base = current_time - Instance.base_datetime
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


def create_from_json(path):
    """
    Read json file and return list of Instance
    :param path: path to file
    :return: list of Instance
    """
    import json
    from jsonschema import validate

    try:
        with open(path, newline='') as f:
            data = json.load(f)
            schema = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "offset": {"type": "integer"},
                        "duration": {"type": "integer"}
                    },
                    "required": ["name", "offset"]
                }
            }
            validate(data, schema)  # will raise ValidationError if .json doesn't match the schema
            instances = []
            for item in data:
                instances.append(Instance(name=item.get("name"),
                                          offset=item.get("offset"),
                                          duration=item.get("duration")))
            return instances
    except IOError as e:
        print(e)
        return []
    except ValidationError as e:
        print(e)
        print("Check .json_example file for valid schema. "
              "Name and offset are required. Duration is optional.")
        return []