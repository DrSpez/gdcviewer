from flask import Flask, jsonify
from subprocess import check_output
import socket

import config

app = Flask(__name__)


@app.route('/')
def index():
    return "GDC-viewer"


@app.route('/get/deployed', methods=['GET'])
def get_deployed():
    
    deployed = {}
    for service in config.services:
        deployed[service] = get_salt_json(service, 'tungsten.deployed')

    return jsonify({'host': socket.gethostname(), 'deployed': deployed})


@app.route('/get/ip_addrs', methods=['GET'])
def get_ip_address():
    
    ip_addrs = {}
    for service in config.services:
        ip_addrs[service] = get_salt_json(service, 'network.ip_addrs')

    return jsonify({'host': socket.gethostname(), 'ip_addrs': ip_addrs})


def get_salt_json(service, command):
    full_command = 'salt -G service:{} {} --out json'.format(service, command)
    return {command: check_output(full_command.split())}


if __name__ == '__main__':
    app.run(debug=True, port=8888, host='0.0.0.0')
