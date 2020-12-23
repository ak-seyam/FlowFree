import math
from typing import List, Tuple


def order_domain_values():
    """ return the available values, order with least-constaining-value heuristic """
    pass


def select_unassigned_variable(csp, assignments: dict, inp):
    """
    Args:
        assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals
        inp: 2d list of the input
    
    Return:
        coords : a random coordinate
    """
    pass


def forward_check():
    pass


def get_domain(coord):
    pass
    # full_domain = [] # TODO

#     point_domain = []
#     for value in full_domain
#         if value


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


def MRV(variables: List) -> List[Tuple[int, int]]:
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
    for coord in variables:
        domain_len = len(get_domain(coord))
        smallest_domain = min(domain_len, smallest_domain)
        if smallest_domain == domain_len:
            selected_coords.append(coord)

    return selected_coords
