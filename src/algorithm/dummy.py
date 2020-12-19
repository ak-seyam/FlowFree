from typing import List
from utils.paths.points_properties import get_item_in_coord, is_empty, search_around
from utils.paths.get_terminals import get_terminals
from model.case import case


def assignment_complete(assignments, inp):
    """
    input:
    assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals
    inp: 2d list of the input

    return weather or not the assignments are complete
    """
    # if len of assignments keys length of inp (rows * columns) - starting points
    # then assignment is complete
    return len(assignments) == (len(inp) * len(inp[0]))


# changed
def select_unassigned_variable(assignments: dict, inp):
    """
    input:
    assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals
    inp: 2d list of the input

    return the next unassigned values or non if no unassigned variable exist
    """
    # TODO (DONE)
    # initially assignments will be terminals
    # select the last one
    # the first empty place should be returned
    assignments_list = list(assignments.keys())
    last_point = assignments_list[-1]
    return search_around(last_point, inp, is_empty)

# changed
# ROI TODO: you can use cached values BUT DON'T DO IT B4 YOU TELL THE WHOLE TEAM


def order_domain_values(csp, assignments, inp, var):
    """
    return the available values
    """
    values = []
    # get values that are not connected yet
    terminals = get_terminals(inp)
    for key in terminals:
        same_color_neighbors_s = search_around(
            terminals[key][0], inp, lambda inp, point: get_item_in_coord(inp, point) == key) != None
        same_color_neighbors_e = search_around(
            terminals[key][1], inp, lambda inp, point: get_item_in_coord(inp, point) == key) != None
        if not (same_color_neighbors_e and same_color_neighbors_s):
            values.append(key)
    return values


# TODO: study consistency to know the paramters you should pass here
def inference():
    """
    return inferences as list or state.faileur
    """
    return case.failure


def is_consistant(assignment: dict, assignments: List[dict], csp):
    """
    return weather or not assignment is consistant with assignments according to the csp
    """
    pass
