from typing import List
from utils.paths.get_terminals import get_terminals
def assignment_complete(assignments,inp):
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

    return the next unassigned values
    """
    # TODO
    # initially assignments will be terminals
    # select the last one
    # the first empty place should be returned
    assignments_list  = list(assignments.keys())
    last_one = assignments_list[-1]
    

# changed
def order_domain_values():
    """
    return the available values
    """
    pass

# TODO: study consistency to know the paramters you should pass here
def inference():
    """
    return inferences as list or state.faileur
    """
    pass

def is_consistant(assignment:dict,assignments:List[dict],csp):
    """
    return weather or not assignment is consistant with assignments according to the csp
    """
    pass