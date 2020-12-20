from typing import List
from utils.paths.points import get_item_in_coord, is_empty, search_around, is_terminals_connect
from utils.paths.initial_state import get_initial_state
from model.case import case
from utils.paths.non_zigzag_path import is_surrounding_square_filled
from random import random


def assignment_complete(assignments, inp):
    """
    input:
    assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals
    inp: 2d list of the input

    return weather or not the assignments are complete
    """
    # if len of assignments keys length of inp (rows * columns) - starting points
    # then assignment is complete
    return len(assignments) >= (len(inp) * len(inp[0]))


# changed
def select_unassigned_variable(csp, assignments: dict, inp):
    """
    input:
    assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals
    inp: 2d list of the input

    return a random coordinate
    """

    # TODO (DONE)
    # initially assignments will be terminals
    # select the last one
    # the first empty place should be returned

    # print("assignents", assignments)
    # assignments_list = list(assignments.keys())
    # if len(assignments_list):
    #     last_point = assignments_list[-1]
    #     return search_around(last_point, assignments, is_empty)[0]
    # else:
    #     terminals = get_initial_state(inp)[0]
    #     first_point = list(terminals.values())[0][0]
    #     return search_around(first_point, assignments, is_empty)[0]

    _tmp = []
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            if assignments.get((i, j)) == None:
                _tmp.append((i, j))
    rand_index = int(random()*len(_tmp) // 1)

    # rand_index_1 = int(random() * len(inp) // 1)
    # rand_index_2 = int(random() * len(inp) // 1)

    return _tmp[rand_index]

# changed
# ROI TODO: you can use cached values BUT DON'T DO IT B4 YOU TELL THE WHOLE TEAM


def order_domain_values(csp, assignments, inp, var):
    """
    return the available values, in the dummy case return all values
    """

    # values = []

    # # get the surrounding values
    # colored_neighbors_coordinates = search_around(
    #     var, assignments, lambda assignments, point: assignments.get(point) != None)

    # for coord in colored_neighbors_coordinates:
    #     values.append(assignments[coord])

    # # remove the totally connected
    # terminals = get_initial_state(inp)[0]

    terminals = get_initial_state(inp)[0]
    return [color.lower() for color in terminals.keys()]
    # return list(terminals.keys())

    # terminals = get_initial_state(inp)[0]
    # for key in terminals:
    #     same_color_neighbors_s = search_around(
    #         terminals[key][0], inp, lambda inp, point: get_item_in_coord(inp, point) == key) != None
    #     same_color_neighbors_e = search_around(
    #         terminals[key][1], inp, lambda inp, point: get_item_in_coord(inp, point) == key) != None
    #     if not (same_color_neighbors_e and same_color_neighbors_s):
    #         values.append(key)
    # return values


# TODO: study consistency to know the paramters you should pass here
def inference():
    """
    return inferences as list or state.faileur
    """

    return case.failure


def is_consistant(current_assignment: dict, assignments: List[dict], inp, csp):
    """
    input:
    current_assignment: the coordinate = value dict 
    assignments: the current assignments w/o current assignmet
    csp: (you violate the constraint be returning true) in dump it is just an array of constrains in dumb it should be just an array with a square case checking 

    return: weather or not assignment is consistant with assignments according to the csp
    """

    # TODO
    # steps
    # - check each constraint in csp they all should result True
    #    if no -> return false, return true otherwise

    # TODO now every constraint is hardcoded this should improved in other backtrack logic
    # NOTE for other is consistant you might use a totally different csp and this
    # is ok

    # if the node already assigned
    # TODO delete
    # if assignments.get(list(current_assignment.keys())[0]) != None:
    #     return False

    # if all surrounding are empty then consistent

    ssf = is_surrounding_square_filled(
        {**assignments, **current_assignment}, inp, list(current_assignment.keys())[0])
    if ssf:
        return False

    color = list(current_assignment.values())[0]
    terminal_connected = is_terminals_connect(
        color, inp, {**assignments, **current_assignment})

    if terminal_connected:
        for coord in list(assignments.keys()):
            if assignments[coord] == color:
                # has 1 empty neighbors or 2 same color neighbors
                empty_neighbors = search_around(
                    coord, inp, assignments, is_empty)
                empty_neighbors_count = len(empty_neighbors)
                same_color_neighbors = search_around(
                    coord, inp, assignments,
                    lambda assi, point: assi.get(point).lower() == color)
                same_color_neighbors_count = len(same_color_neighbors)
                if not(empty_neighbors_count == 1 or same_color_neighbors_count == 2):
                    return False
    
    # weather or not any point had the same color
    # surrounded_points = search_around(list(current_assignment.keys())[0], assignments, lambda assign, point: False if assign.get(
    #     point) == None else assign.get(point) == list(current_assignment.values())[0])

    # if len(surrounded_points) == 0:
    #     return False

    return True
