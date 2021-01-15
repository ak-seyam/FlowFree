from typing import List
from utils.paths.points import get_item_in_coord, is_empty, search_around, is_terminals_connect, get_same_color_neighbors, get_neighbors_coords
from model.case import case
from utils.paths.path_state import is_good_combination, terminal_with_two_same_color_exist, is_neighbors_terminal_have_vaild_path
from random import random, shuffle

config = {
    "totally_random" : False
}

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


def get_var(initial_state, assignments, inp, connected_terminals, *args):
    var = select_unassigned_variable(None,
                                     assignments, inp)  # TODO Room for improvement
    return var, None

# changed


def select_unassigned_variable(variables_domain, assignments: dict, inp):
    """
    input:
    assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals
    inp: 2d list of the input

    return a random coordinate
    """

    _tmp = []
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            if assignments.get((i, j)) == None:
                if config.get("totally_random"):
                    _tmp.append((i, j))
                else :
                    return (i,j)

    rand_index = int(random()*len(_tmp) // 1)

    return _tmp[rand_index]


def order_domain_values(initial_state, assignments, inp, var, variables_domain, *arg):
    """
    return the available values, in the dummy case return all values
    """

    terminals = initial_state[0]
    colors = [color.lower() for color in terminals.keys()]
    shuffle(colors)
    return colors


def inference():
    """
    return inferences as list or state.faileur
    """
    return case.failure


def is_consistant(initial_state, current_assignment: dict, assignments: List[dict], inp, connected_terminals):
    """
    input:
    current_assignment: the coordinate = value dict 
    assignments: the current assignments w/o current assignmet

    return: weather or not assignment is consistant with assignments 
    """

    current_assignment_color = list(current_assignment.values())[0]
    current_assignment_coord = list(current_assignment.keys())[0]

    # check if already marked point will be in the path

    # Combination check
    good_comb = is_good_combination(current_assignment_coord, assignments, inp)
    if not good_comb:
        return False

    # select
    '''
    # for terminals check wheather or not they have more than one similar neighbor
    >  we don't need to check all the terminals every time only the connected ones see @issue

    #terminal_with_two_neighbors = terminal_with_two_same_color_exist(initial_state,assignments,inp)
    #if terminal_with_two_neighbors :
    #    return False
    '''
    # for connected terminals check wheather or not they have more than one similar neighbor
    if not is_neighbors_terminal_have_vaild_path(
            current_assignment_coord, initial_state, assignments, inp):
        return False

    terminal_connected = current_assignment_color.upper() in connected_terminals

    if terminal_connected:
        return False
    return True
