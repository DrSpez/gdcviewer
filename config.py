import os
import yaml


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DB_DIR = os.path.join(ROOT_DIR, '.gdc')
DB_FILE = os.path.join(DB_DIR, 'database.json')
MINIONS_FILE = os.path.join(DB_DIR, 'minions.yaml')

debug = True

services = ['esbuild', 'api', 'api-legacy', 'portal', 'legacy-portal', 'signpost']

minions = yaml.safe_load(open(MINIONS_FILE, 'r'))
minion_port = 8888

master_host = '0.0.0.0'
master_port = 5000
