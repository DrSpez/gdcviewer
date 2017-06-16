import requests
from flask import Flask, render_template

import config

app = Flask(__name__)


@app.route('/')
def index():
    # minion_ips = get_minion_info('ip_addrs')
    # minion_deployed = get_minion_info('deployed')

    minion_ips = {}
    minion_deployed = {}
    test_data = [{'label': 'Nightly',
                  'host_name': 'nightly-av2-salt-master',
                  'host_ip': '123.13.123.45',
                  'services': {'esbuild': [{'host_name': 'nightly-esbuild-0',
                                            'host_ip': '123.43.123.43',
                                            'deployed': '2q12efast43tfsv'},
                                           {'host_name': 'nightly-esbuild-1',
                                            'host_ip': '123.43.123.44',
                                            'deployed': '2q12efast43tfsv'},
                                           ],
                               'api': [{'host_name': 'nightly-api-1',
                                        'host_ip': '123.43.132.44',
                                        'deployed': 'dsfg8asdvacsvc'}],
                               'api-legacy': []}
                  },
                  {'label': 'UAT',
                    'host_name': 'uat-av2-salt-master',
                    'host_ip': '123.25.231.41',
                    'services': {'esbuild': [{'host_name': 'uat-esbuild-0',
                                              'host_ip': '123.25.241.43',
                                              'deployed': 'asdfzxcvzx0'},
                                             {'host_name': 'uat-esbuild-1',
                                              'host_ip': '123.43.123.44',
                                              'deployed': 'asdfzxcvzx0'},
                                             ],
                                 'api': [],
                                 'api-legacy': [{'host_name': 'uat-api-legacy',
                                                 'host_ip': '123.43.123.11',
                                                 'deployed': '4sdf9zxcv9vsdf'}],
                                }
                  },
                ]

    return render_template('index.html', data=test_data, ips=minion_ips,
                           deployed=minion_deployed)


def get_minion_info(endpoint):
    assert endpoint in ['ip_addrs', 'deployed']
    info_map = {}
    for minion_ip in config.minions:
        url = 'http://{}:{}/get/{}'.format(minion_ip,
                                            config.minion_port, endpoint)
        print url
        info_map[minion_ip] = requests.get(url).text
    return info_map


if __name__ == '__main__':
    app.run(host=config.master_host, port=config.master_port,
            debug=config.debug)
