from flask import Flask, jsonify
from flask import request, send_from_directory

import json
import dataclasses
import pickle

from reader.reader import read_inputfile
from algorithm.backtrack import backtrack
from algorithm import dummy as dum
from algorithm import smart
from utils.paths.initial_state import get_initial_state
from utils.formater import formatter, formatter
from random import seed

app = Flask(__name__)


path = "../input/input{map_num}.txt"


@app.route('/')
def hello():
    return send_from_directory('static', 'index.html')


@app.route('/map/<string:map_num>')
def map(map_num):
    '''    
    suported maps:
        - 10101
        - 10102
        - 1212
        - 1214
        - 1414
        - 55
        - 77
        - 88
        - 991
    '''
    inp = read_inputfile(path.format(map_num=map_num))

    height = len(inp)
    width = len(inp[0])
    return jsonify(height=height, width=width)


@app.route('/map/sol/<string:map_num>')
def solution(map_num):
    inp = read_inputfile(path.format(map_num=map_num))
    initial_state = get_initial_state(inp)
    res = backtrack(
        initial_state,
        initial_state[1],
        inp,
        smart.order_domain_values,
        dum.assignment_complete,
        dum.inference,
        dum.is_consistant,
        lambda assignments: 1,  # for testing only
        smart.get_var
    )
    point_list = []
    for i, coord in enumerate(res):
        point_list.append({'x': coord[0],
                           'y': coord[1], 'color': res[coord]})
    return jsonify(point_list)


# NOTE for map visit /index.html
if __name__ == "__main__":

    app.run(debug=True)
