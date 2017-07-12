import os
import yaml


class BaseConfig:
    debug = True

    ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
    SECRET_DIR = os.path.join(ROOT_DIR, '.gdc')
    SERVICES = {
                'esbuild': 'esbuild', 'api': 'gdcapi', 'api-legacy': 'gdcapi',
                'postgres': 'postgres-cloner', 'signpost': 'signpost',
                'portal': 'portal-ui', 'legacy-portal': 'portal-ui-legacy',
                }
    ENDPOINTS = ['ip_addrs', 'deployed']
    HOST = '0.0.0.0'


class MinionConfig(BaseConfig):
    def __init__(self):
        self.PORT = 8888


class MasterConfig(BaseConfig):
    def __init__(self):
        self.PORT = 1234
        self.MINION_PORT = MinionConfig().PORT

        self.MINIONS_FILE = os.path.join(BaseConfig.SECRET_DIR, 'minions.yaml')
        self.DB_FILE = os.path.join(BaseConfig.SECRET_DIR, 'database.json')

        self.MINIONS = yaml.safe_load(open(self.MINIONS_FILE, 'r'))

