from flask import Flask, jsonify, render_template
import subprocess
import socket
import json

from config import MinionConfig

config = MinionConfig()
app = Flask(__name__)
HOSTNAME = socket.gethostname()


@app.route('/')
def index():
    return render_template('minion_index.html', host_name=HOSTNAME)


@app.route('/get/deployed', methods=['GET'])
def get_deployed():
    
    deployed = {}
    for service in config.SERVICES:
        response = get_salt_json(service, 'tungsten.deployed')
        if response != {}:
            deployed[service] = response

    return jsonify({'host_name': HOSTNAME, 'deployed': deployed})


@app.route('/get/ip_addrs', methods=['GET'])
def get_ip_address():
    
    ip_addrs = {}
    for service in config.SERVICES:
        response = get_salt_json(service, 'network.ip_addrs')
        if response != {}:
            ip_addrs[service] = response

    return jsonify({'host_name': HOSTNAME, 'workers': ip_addrs})


def get_salt_json(service, command):
    full_command = 'salt -G service:{} {} --out json --static'.format(service, command)
    try:
        cmd_output = subprocess.check_output(full_command.split())
        output = json.loads(cmd_output)
    except subprocess.CalledProcessError:
        output = {}
    except Exception as err:
        output = {'error': repr(err)}

    return output


if __name__ == '__main__':
    app.run(debug=config.debug, port=config.PORT, host=config.HOST)
