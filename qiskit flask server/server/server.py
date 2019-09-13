#!/usr/bin/env python3
from pathlib import Path
import sys
import logging

# add project path to PYTHONPATH in order to run server.py as a script
project_path = str(Path().resolve().parent)
sys.path.append(project_path)

from flask import request
from flask import Flask
from flask_cors import CORS

from api import qasm, statevector, measurement


app = Flask(__name__)
CORS(app)

logging.getLogger('flask_cors').level = logging.DEBUG # for debugging


@app.route('/')
def welcome():
    return "Hi Qiskiter!"


@app.route('/api/run/qasm', methods=['GET'])
def run_qasm():
    qasm_string = request.args['qasm']
    backend = request.args['backend']
    print("--------------")
    print('qasm: ', qasm_string)
    print('backend: ', backend)
    print("^^^^^^^^^^^^^^")
    output = qasm(qasm_string, backend)
    ret = {"result": output}
    return jsonify(ret)


@app.route('/api/run/get_statevector', methods=['POST'])
def get_statevector():
    circuit_dimension = request.form.get('circuit_dimension')
    gate_string = request.form.get('gate_array')
    print("--------------")
    print(gate_string)

    reply = statevector(circuit_dimension, gate_string)
    return reply


@app.route('/api/run/do_measurement', methods=['POST'])
def do_measurement():
    circuit_dimension = request.form.get('circuit_dimension')
    gate_string = request.form.get('gate_array')
    print("--------------")
    print(gate_string)

    reply = measurement(circuit_dimension, gate_string)
    return reply


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8008)
