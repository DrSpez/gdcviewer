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
    commands = {s: 'salt -G service:{} tungsten.deployed --out json'.format(s)
                for s in config.services}
    # commands = {'date service': 'date', 'ls service': 'ls',
    #             'la service': 'ls -a', 'lt service': 'ls -t'}
    deployed = {s: check_output(cmd.split()) for s, cmd in commands.items()}

    return jsonify({'host': socket.gethostname(), 'deployed': deployed})


if __name__ == '__main__':
    app.run(debug=True)
