# NOTE: inp is 2d list of chars/strings represents the input

from typing import Tuple, List
from model.directions import direction as d
from utils.paths.points import get_item_in_coord, search_around, points_are_equal, get_path, get_neighbors_coords, is_empty, check_for_good_combinations


def get_square_coordinates(current_index: Tuple[int, int], corners):
    """
    input: 
    current index: (x,y):tuple
    corners: dict with keys resembles corners
    return the "<= 4" squares (square is a dict containing the four indices of the cells to check)
    containing the current index 
    """
    # prepares squares to order
    order = {
        (d.north, d.east): [current_index,  # same point
                            # the one to the east
                            (current_index[0]+1, current_index[1]),
                            # the one to the north
                            (current_index[0], current_index[1]-1),
                            # the one to the north east
                            (current_index[0]+1, current_index[1]-1),
                            ],
        (d.north, d.west): [current_index,  # same point
                            # the one to the west
                            (current_index[0]-1, current_index[1]),
                            # the one to the north
                            (current_index[0], current_index[1]-1),
                            # the one to the north west
                            (current_index[0]-1, current_index[1]-1),
                            ],
        (d.south, d.west): [current_index,  # same point
                            # the one to the west
                            (current_index[0]-1, current_index[1]),
                            # the one to the south
                            (current_index[0], current_index[1]+1),
                            # the one to the south west
                            (current_index[0]-1, current_index[1]+1),
                            ],
        (d.south, d.east): [current_index,  # same point
                            # the one to the east
                            (current_index[0]+1, current_index[1]),
                            # the one to the south
                            (current_index[0], current_index[1]+1),
                            # the one to the south east
                            (current_index[0]+1, current_index[1]+1),
                            ]
    }
    # 1- elemination
    # north squares
    if current_index[1]-1 <= corners[d.north]:
        keys = list(order.keys())
        for key in keys:
            if d.north in key:
                del order[key]
    # south squares
    if current_index[1]+1 >= corners[d.south]:
        keys = list(order.keys())
        for key in keys:
            if d.south in key:
                del order[key]
    # west squares
    if current_index[0]-1 <= corners[d.west]:
        keys = list(order.keys())
        for key in keys:
            if d.west in key:
                del order[key]
    # east squares
    if current_index[0]+1 >= corners[d.east]:
        keys = list(order.keys())
        for key in keys:
            if d.east in key:
                del order[key]

    return list(order.values())


def is_surrounding_square_filled(assignment, inp, current_index):
    """
    input:
    assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals
    inp: 2d list of the input

    return wheather or not any of the surrounding squares is filled
    """

    # TODO (DONE)
    # input -> assignment
    # search in assignments for the square coordinates
    # if all exist and have the same value
    # then return true

    # defining corners
    corners = {
        d.north: -1,
        d.south: len(inp),
        d.east: len(inp),
        d.west: -1
    }

    # TODO change this to coord (DONE)
    surrounding_squares = get_square_coordinates(current_index, corners)

    # current_index_letter = get_item_in_coord(inp, current_index)
    current_index_letter = assignment[current_index]

    # check if we have the same letter in any one of the surrounding squares
    for square in surrounding_squares:
        has_sur_square_filled = True
        for coord in square:
            value_in_assignment = assignment.get(coord) 
            if value_in_assignment != None:
                # has_sur_square_filled = has_sur_square_filled and (
                #     value_in_assignment == current_index_letter)
                if value_in_assignment.lower() != current_index_letter.lower():
                    has_sur_square_filled = False
                    break
            else:
                has_sur_square_filled = False
                break
        if has_sur_square_filled:
            return True

    return False

def is_good_combination(current_assignment_coord, assignments,inp):
    """
    check the combination (position) of the current assignment point as well as the surrounding points
    """
    comb_points_of_interest = [current_assignment_coord]
    comb_points_of_interest.extend(get_neighbors_coords(current_assignment_coord, inp))
    for coord in comb_points_of_interest:
        if is_empty(assignments, coord) or assignments[coord].isupper():
            continue
        good_comb = check_for_good_combinations(coord,assignments[coord],assignments,inp)
        if not good_comb :
            return False
    
    return True

def is_neighbors_terminal_have_vaild_path(current_assignment_coord, initial_state, assignments, inp):
    terminals = initial_state[0]

    terminal_neighbors_coords = search_around(
        current_assignment_coord, inp, assignments,
        lambda assign, point: assign.get(point, '').isupper() # empty and assigned points will be false only terminals will pass
    )
    for coord in terminal_neighbors_coords:
        # empty and assigned points will be false only terminals will pass
        if assignments.get(coord,  '').isupper():
        terminal_color = assignments[coord]
        similar_neighbors = len(search_around(coord, inp, assignments,
                                              lambda assign, point: assign.get(point, '').upper() == terminal_color))
        empty_neighbors = len(search_around(coord, inp, assignments,
                                            is_empty))
        valid_state = similar_neighbors == 1 or (

            similar_neighbors == 0 and empty_neighbors >= 1)
        if not valid_state:
            return False
    return True


def terminal_with_two_same_color_exist(current_assignment_coord, initial_state, assignments, inp):
    '''#deprcated use instead @is_neighbors_terminal_have_vaild_path'''
    terminals = initial_state[0]
    # old slow implementation
    for terminal in terminals:
        similar_neighbors_start = search_around(terminals[terminal][0], inp, assignments,
                                                lambda assign, point: False if assign.get(point) == None else assign[point].upper() == terminal)
        number_of_similar_neighbors_start = len(similar_neighbors_start)

        similar_neighbors_end = search_around(terminals[terminal][1], inp, assignments,
                                              lambda assign, point: False if assign.get(point) == None else assign[point].upper() == terminal)
        number_of_similar_neighbors_end = len(similar_neighbors_end)
        if number_of_similar_neighbors_start > 1 or number_of_similar_neighbors_end > 1:
            return True
    return False
