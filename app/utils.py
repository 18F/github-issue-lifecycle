import datetime
import json

import yaml


def to_py_datetime(timestamp_string):
    if timestamp_string:
        return datetime.datetime.strptime(timestamp_string,
                                          '%Y-%m-%dT%H:%M:%SZ')
    else:
        return None


def permissive_yaml_load(txt):
    txt = txt.replace('\t', ' ')
    txt = txt.strip(' -\n')
    return yaml.load(txt)


class ISO8601JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)
