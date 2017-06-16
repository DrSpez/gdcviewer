import requests
from flask import Flask, render_template

import config
import test_data


app = Flask(__name__)


@app.route('/')
def index():
    data = get_data()

    return render_template('master_index.html', data=data)


def get_data():
    minion_ips = query_get('ip_addrs')
    minion_deployed = query_get('deployed')

    data = test_data.data
    return data


def query_get(endpoint):
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
