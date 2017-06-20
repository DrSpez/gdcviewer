import os
import json

import config


def init_database():
    # Create .gdc/ directory if it does not exist
    if not os.path.isdir(config.DB_DIR):
        os.mkdir(config.DB_DIR)

    # Check if minions.yaml exists
    if not os.path.isfile(config.MINIONS_FILE):
        raise Exception('Create `.gdc/minions.yaml` with `Cluster label: salt_master_ip` pairs!')

    # Create database file if does not exist:
    if not os.path.isfile(config.DB_FILE):
        open(config.DB_FILE, 'w').close()


def read_data():
    try:
        return json.loads(open(config.DB_FILE, 'r').read())
    except:
        return {}


def save_data(data):
    old_data = read_data()

    for doc in data:
        old_data[doc['label']] = doc

    with open(config.DB_FILE, 'w') as f:
        f.write(json.dumps(old_data))

    return old_data


if __name__ == '__main__':
    data = save_data([{'label': 'my', 'lol': {'asdf': 1234}},
                      {'label': 'ik', 'lol': {'asdf': 4321}}])

