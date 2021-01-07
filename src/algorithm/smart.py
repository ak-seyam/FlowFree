from pprint import pprint
import math
from typing import List, Tuple, Dict
from algorithm.dummy import is_consistant
from model.case import case
from utils.paths.points import get_constrained_nighbours
import copy


def order_domain_values(initial_state, assignments, inp, var, variables_domain):
    """ return the available values, order with least-constaining-value heuristic """
    return variables_domain[var]
    
    # use least-constaining-value
    # is actully slower 🤷‍♀
    # if len(variables_domain[var]) > 1:
    #     ordered_domain = least_constraining_value(initial_state, assignments,
    #                                               var, variables_domain, inp)
    #     return ordered_domain
    # else:
    #     return variables_domain[var]


def free_vars(assignments, inp):
    available_vars = []
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            if assignments.get((j, i)) == None:
                available_vars.append((j, i))
    return available_vars

def inference():
    """
    return inferences as list or state.faileur
    """

    return case.failure


def get_var(initial_state , assignments, inp, connected_terminals ,prev_domain,prev_variable,prev_value,prev_connected_terminal):
    """
    docstring
    """
    fv = free_vars(assignments, inp)
    variables_domain = get_available_domain_multiple(
        initial_state, fv, assignments, inp, connected_terminals,prev_domain,prev_variable,prev_value,prev_connected_terminal)
    
    if not forward_check(variables_domain):
        return case.failure
        
    var = select_unassigned_variable(variables_domain,
                                     assignments, inp)  
    return var, variables_domain

def select_unassigned_variable(variables_domain , assignments: dict, inp):
    """
    Args:
        assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals
        inp: 2d list of the input

    Return:
        coords : return coordinatation with mrv
    """
    smallest_domains = MRV(variables_domain)
    return smallest_domains[0]


def forward_check(variables_domain):
    ''' forward check for empty domains return true if no empty domains'''
    for coords in variables_domain:
        if len(variables_domain[coords]) == 0:
            return False

    return True


def get_available_domain_multiple(initial_state, variables, assignments, inp, connected_terminals,prev_domain,prev_variable,prev_value,prev_connected_terminal):
    variables_domain = {}
    connection_changed = len(connected_terminals) > len(prev_connected_terminal)
    first_run = prev_variable == None
    if connection_changed or first_run:
        # update all variables
        for coord in variables:
            domain = get_available_domain(
                initial_state, coord, assignments, inp,connected_terminals)
            variables_domain[coord] = domain
    else:
        variables_domain = copy.deepcopy(prev_domain)
        del variables_domain[prev_variable]
        big_nighbours = get_constrained_nighbours(prev_variable,inp,assignments )
        for coord in big_nighbours:
            domain = get_available_domain(
                initial_state, coord, assignments, inp,connected_terminals)
            variables_domain[coord] = domain
    return variables_domain


def get_available_domain(initial_state, coord, assignments, inp, connected_terminals):
    """ return list of values that satisfy the constrains for selected coord

    example assigning one value for terminal the othe domain will be reduced
    >>> from reader.reader import read_inputfile
    >>> from utils.paths.points import get_initial_state
    >>> paths = ["../input/input55.txt"]
    >>> inp = read_inputfile(paths[0])
    >>> initial_state = get_initial_state(inp)
    >>> assignments = {(0,1): 'b'}
    >>> coord = (1,0)
    >>> get_available_domain(initial_state, coord, assignments, inp)
    ['r', 'o', 'y', 'g']
    """
    terminals = initial_state[0]
    colors = [color.lower() for color in terminals.keys()]
    full_domain = colors

    point_domain = []
    for value in full_domain:
        # add val to check constrain
        assignments[coord] = value
        if is_consistant(initial_state, {coord: value},  assignments, inp, connected_terminals ):
            point_domain += value
        del assignments[coord]

    return point_domain


def degree_heuristic(variables: List,inp , assignments) -> List[Tuple[int, int]]:
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
    most_constraining_var = variables[0]
    most_constraining_count = -math.inf
    for coord in variables:
        constrained_count = len(get_constrained_nighbours(coord,inp, assignments))
        if constrained_count > most_constraining_count:
            most_constraining_count = constrained_count
            most_constraining_var = coord
    return most_constraining_var


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


def least_constraining_value(initial_state, assignments, coord, variables_domain, inp, connected_terminals):
    ''' value selection heuristic whitch count the order the values by number of constrains with 
    smallest first  
    '''

    smallest_number_of_constraints = math.inf
    count_value_ordered = []

    variables = free_vars({**{coord: 'holder'}, **assignments}, inp)
    domain = variables_domain[coord]
    for value in domain:
        updated_connected_terminals = connected_terminals = refresh_connected_terminals(
                {coord: value}, {**{coord: value}, **assignments}, connected_terminals, initial_state, inp)
        updated_variable_domains = get_available_domain_multiple(
            initial_state, variables, {**{coord: value}, **assignments}, inp, updated_connected_terminals,
             variables_domain, coord, None, connected_terminals)
        count_constrained = 0
        
        for coord in updated_variable_domains:
            if len(updated_variable_domains[coord]) < len(variables_domain[coord]):
                count_constrained += 1

        count_value_ordered.append((count_constrained, value))

    count_value_ordered.sort()
    order_domain_values = []
    for count, value in count_value_ordered:
        order_domain_values += value

    return order_domain_values
