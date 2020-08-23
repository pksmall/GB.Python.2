import json
import datetime

CONF_FILE = '.config.json'
confJson = None


def load_config():
    global confJson

    with open("./" + CONF_FILE) as f_n:
        f_n_content = f_n.read()
        confJson = json.loads(f_n_content)


def date(unixtime, format='%Y-%m-%d %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)


# config
load_config()
