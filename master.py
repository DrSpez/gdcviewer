import requests
import json
from flask import Flask, render_template

import config
import test_data


app = Flask(__name__)


@app.route('/')
def index():
    data = get_data()

    return render_template('master_index.html', data=data)


def get_data():
    data = []
    for minion_ip in config.minions:
        minion_ips = query_get('ip_addrs', minion_ip)
        minion_deployed = query_get('deployed', minion_ip)

        host_name = minion_ips['host_name']
        label = host_name.split('-')[1].upper()

        services_info = {}
        for service, workers_data in minion_ips['workers'].items():
            services_info.setdefault(service, [])
            for worker, worker_ip in workers_data.items():
                services_info[service].append({
                    'host_name': worker,
                    'host_ip': worker_ip,
                    'deployed': minion_deployed['deployed'][service][worker]
                    })

        cluster_data = {'label': label,
                        'host_name': host_name,
                        'host_ip': minion_ip,
                        'services': services_info}
        data.append(cluster_data) 

    return data


def query_get(endpoint, minion_ip):
    assert endpoint in ['ip_addrs', 'deployed']
    url = 'http://{}:{}/get/{}'.format(minion_ip, config.minion_port, endpoint)
    print url
    return requests.get(url).json()


if __name__ == '__main__':
    app.run(host=config.master_host, port=config.master_port,
            debug=config.debug)
