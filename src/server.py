from flask import Flask, jsonify
from flask import request, send_from_directory
from flask_socketio import SocketIO
from flask_socketio import send, emit

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
from time import sleep
import threading
from enum import Enum

app = Flask(__name__)
socketio = SocketIO(app)


class solver_state(Enum):
    free = 0
    locked = 1
    in_demand = 2


dump_sesssion = {'send_more': False,
                
                
                 'solver_state': solver_state.free, 'in_demand': False}

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


def assigment_to_point(assigments):
    point_list = []
    for i, coord in enumerate(assigments):
        point_list.append({'x': coord[0],
                           'y': coord[1], 'color': assigments[coord]})

    return point_list


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
        lambda assignments: 1,
        smart.get_var
    )
    point_list = assigment_to_point(res)
    return jsonify(point_list)


def draw_with_delay(assignments, delay):
    if dump_sesssion['in_demand']:
        return
    while not dump_sesssion['send_more']:
        sleep(.11)

    socketio.emit(
        "assigment", assigment_to_point(assignments))
    # sleep(delay)
    dump_sesssion['send_more'] = False


@socketio.on('send_more')
def control_animation(send_permession):
    dump_sesssion['send_more'] = send_permession
    # print("send_more", send_permession)


@socketio.on('animate')
def solution_animated(map_num):
    # make sure no other session is running
    if dump_sesssion['solver_state'] == solver_state.locked:
        dump_sesssion['in_demand'] = True
        while dump_sesssion['solver_state'] == solver_state.locked:
            sleep(0.3)

    dump_sesssion['in_demand'] = False
    # hold current session
    dump_sesssion['solver_state'] = solver_state.locked

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
        lambda assignments: draw_with_delay(assignments, .1),
        smart.get_var
    )
    socketio.emit('done', 'done')

    # free session
    dump_sesssion['solver_state'] = solver_state.free


# NOTE for map visit /index.html
if __name__ == "__main__":

    socketio.run(app, debug=True)
