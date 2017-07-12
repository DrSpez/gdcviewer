import requests
import multiprocessing
import time
import json
import re
from flask import Flask, render_template, request

import database as db
import test_data
from config import MasterConfig

config = MasterConfig()
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        data = get_data()
    else:
        data = db.read_data().values()

    return render_template('master_index.html', data=data, services=config.SERVICES)


def get_data():
    # Run get requests concurrently:
    print "\nRetrieving cluster data:"
    start_time = time.time()
    n_processes = len(config.ENDPOINTS) * len(config.MINIONS)
    pool = multiprocessing.Pool(processes=n_processes)

    inputs = [(endpoint, minion_ip) for endpoint in config.ENDPOINTS
                                    for minion_ip in config.MINIONS.values()]
    outputs = pool.map(query_get, inputs)
    print "\nData retrieved in {} sec\n".format(time.time() - start_time)

    # Transform outputs to required data structure:
    data = []
    for minion_name, minion_ip in config.MINIONS.items():
        ip_index = [i for i, v in enumerate(inputs)
                    if v[0] == 'ip_addrs' and v[1] == minion_ip][0]
        deployed_index = [i for i, v in enumerate(inputs)
                          if v[0] == 'deployed' and v[1] == minion_ip][0]

        minion_ips = outputs[ip_index]
        minion_deployed = outputs[deployed_index]

        host_name = minion_ips['host_name']
        label = host_name.split('-')[1].upper()

        services_info = {}
        for service, workers_data in minion_ips['workers'].items():
            services_info.setdefault(service, [])
            for worker, worker_ip in workers_data.items():
                worker_ip = ', '.join(re.compile('[\d+\.]+').findall(str(worker_ip)))
                services_info[service].append({
                    'host_name': worker,
                    'host_ip': worker_ip,
                    'deployed': minion_deployed['deployed'][service][worker]
                    })

        cluster_data = {'label': minion_name,
                        'host_name': host_name,
                        'host_ip': minion_ip,
                        'services': services_info}
        data.append(cluster_data) 

    # Update database with new data:
    db.save_data(data)

    return data


def query_get((endpoint, minion_ip)):
    session = requests.session()
    assert endpoint in config.ENDPOINTS
    url = 'http://{}:{}/get/{}'.format(minion_ip, config.MINION_PORT, endpoint)
    print '->', url
    return session.get(url).json()


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT,
            debug=config.debug)
