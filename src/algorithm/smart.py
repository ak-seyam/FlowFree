import math
from typing import List, Tuple, Dict
from algorithm.dummy import is_consistant
from model.case import case


def order_domain_values(initial_state, csp, assignments, inp, var, variables_domain):
    """ return the available values, order with least-constaining-value heuristic """
    # TODO use least-constaining-value
    return variables_domain[var]


def free_vars(assignments, inp):
    available_vars = []
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            if assignments.get((i, j)) == None:
                available_vars.append((i, j))
    return available_vars

def inference():
    """
    return inferences as list or state.faileur
    """

    return case.failure


def get_var(initial_state , csp , assignments, inp ):
    """
    docstring
    """
    fv = free_vars(assignments, inp)
    variables_domain = get_available_domain_multiple(
        initial_state, fv, assignments, inp,  csp)

    if not forward_check(variables_domain):
        return case.failure
        
    var = select_unassigned_variable(variables_domain,
                                     csp, assignments, inp)  
    return var, variables_domain

def select_unassigned_variable(variables_domain, csp, assignments: dict, inp):
    """
    Args:
        assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals
        inp: 2d list of the input

    Return:
        coords : a random coordinate
    """
    smallest_domains = MRV(variables_domain)
    return smallest_domains[0]


def forward_check(variables_domain):
    ''' forward check for empty domains return true if no empty domains'''
    for coords in variables_domain:
        if len(variables_domain[coords]) == 0:
            return False

    return True


def get_available_domain_multiple(initial_state, variables, assignments, inp,  csp):
    variables_domain = {}
    for coord in variables:
        domain = get_available_domain(
            initial_state, coord, assignments, inp,  csp)
        variables_domain[coord] = domain

    return variables_domain


def get_available_domain(initial_state, coord, assignments, inp,  csp):
    """ return list of values that satisfy the constrains for selected coord

    example assigning one value for terminal the othe domain will be reduced
    >>> from reader.reader import read_inputfile
    >>> from utils.paths.points import get_initial_state
    >>> paths = ["../input/input55.txt"]
    >>> inp = read_inputfile(paths[0])
    >>> initial_state = get_initial_state(inp)
    >>> assignments = {(0,1): 'b'}
    >>> coord = (1,0)
    >>> csp = None
    >>> get_available_domain(initial_state, coord, assignments, inp,csp)
    ['r', 'o', 'y', 'g']
    """
    terminals = initial_state[0]
    colors = [color.lower() for color in terminals.keys()]
    full_domain = colors

    point_domain = []
    for value in full_domain:
        # add val to check constrain
        assignments[coord] = value
        if is_consistant(initial_state, {coord: value},  assignments, inp, csp):
            point_domain += value
        del assignments[coord]

    return point_domain


def degree_heuristic(variables: List) -> List[Tuple[int, int]]:
    ''' variable selection heuristic witch choose the variable witch involve in
    most number of variables _ maybe used as tie breaker

    Args:
        variables : available variables to choose from

    Returns:
        coords : the coords with smallest number of available values

    Depends:
        get_constained_number 
    '''
    # loop throw variables
    # get the number of constrains
    # choose the variable with largest number of constrains


def MRV(variables_domain: Dict[Tuple[int, int], List[str]]) -> List[Tuple[int, int]]:
    ''' variable selection heuristic witch choose the variable with Minimum remaining values
    Args:
        variables : available variables to choose from

    Returns:
        coords : the coords with smallest number of available values

    Depends:
        get_domain 
    '''

    smallest_domain = math.inf
    selected_coords = []
    for coord in variables_domain:
        domain_len = len(variables_domain[coord])

        if domain_len < smallest_domain:
            selected_coords = []
            smallest_domain = domain_len

        if smallest_domain == domain_len:
            selected_coords.append(coord)

    return selected_coords


def least_constraining_value(assignments, coord, domain):
    ''' value selection heuristic whitch count the order the values by number of constrains with 
    smallest first  
    '''

    smallest_number_of_constraints = math.inf
    count_value_ordered = []
    for value in domain:
        count = 0
        count += count_is_surrounding_square_filled(
            {**{coord: value}, **assignments}, coord, value)
        count_value_ordered.append(count, value)

    count_value_ordered.sort()
    order_domain_values = []
    for count, value in count_value_ordered:
        order_domain_values += value

    return order_domain_values
