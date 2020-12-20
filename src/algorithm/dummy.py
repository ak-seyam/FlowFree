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
def select_unassigned_variable(csp,assignments: dict, inp):
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
    print("assignents", assignments)
    assignments_list = list(assignments.keys())
    if len(assignments_list) :
        last_point = assignments_list[-1]
        return search_around(last_point, inp, is_empty)
    else :
        terminals = get_terminals(inp)
        first_point = list(terminals.values())[0][0]
        return search_around(first_point,inp,is_empty)

# changed
# ROI TODO: you can use cached values BUT DON'T DO IT B4 YOU TELL THE WHOLE TEAM


def order_domain_values(csp, assignments, inp, var):
    """
    return the available values, in the dummy case return all values that are not connected yet
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


def is_consistant(current_assignment: dict, assignments: List[dict], inp, csp):
    """
    input:
    current_assignment: the coordinate = value dict 
    assignments: the current assignments w/o current assignmet
    csp: in dump it is just an array of constrains in dumb it should be just an array with a square case checking 

    return: weather or not assignment is consistant with assignments according to the csp
    """

    # TODO
    # steps
    # - check each constraint in csp they all should result True
    #    if no -> return false, return true otherwise
    for constraint in csp:
        # add the current assignment to assignments without mutating assignments
        # to do any furthur color checks base of the current location
        constraint({**assignments, **current_assignment},
                   inp, list(current_assignment.keys())[0])
    return True
