import os
import yaml


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
SECRET_DIR = os.path.join(ROOT_DIR, '.gdc')
MINIONS_FILE = os.path.join(SECRET_DIR, 'minions.yaml')
DB_FILE = os.path.join(SECRET_DIR, 'database.json')

debug = True

services = {'esbuild': 'esbuild', 'api': 'gdcapi', 'api-legacy': 'gdcapi',
            'portal': 'portal-ui', 'legacy-portal': 'portal-ui-legacy',
            'signpost': 'signpost'}
endpoints = ['ip_addrs', 'deployed']

minions = yaml.safe_load(open(MINIONS_FILE, 'r'))
minion_port = 8888

master_host = '0.0.0.0'
master_port = 1234
