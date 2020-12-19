# NOTE: inp is 2d list of chars/strings represents the input 

from typing import Tuple, List
from model.directions import direction as d
from get_item_in_coord import get_item_in_coord


def mark_non_zigzag_path(inp: List[list], start_pos: Tuple[int, int]):
    """
    annotate the path in inp with values of non zigzag path
    """
    pass


def get_square_indices(current_index: Tuple[int, int], corners):
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
        for key in order:
            if d.north in key:
                del order[key]
    # south squares
    if current_index[1]+1 >= corners[d.south]:
        for key in order:
            if d.south in key:
                del order[key]
    # west squares
    if current_index[0]-1 <= corners[d.west]:
        for key in order:
            if d.west in key:
                del order[key]
    # east squares
    if current_index[0]+1 >= corners[d.east]:
        for key in order:
            if d.east in key:
                del order[key]

    return list(order.values())


def surrounding_square_filled(inp, current_index):

    # defining corners
    corners = {
        d.north: -1,
        d.south: len(inp),
        d.east: len(inp),
        d.west: -1
    }

    surrounding_squares = get_square_indices(current_index, corners)

    current_index_letter = get_item_in_coord(inp, current_index)

    # check if we have the same letter in any one of the surrounding squares
    for square in surrounding_squares:
        has_sur_square_filled = True
        for coord in square:
            has_sur_square_filled = has_sur_square_filled and (
                get_item_in_coord(inp, coord) == current_index_letter)
        if has_sur_square_filled :
            return True
    
    return False

def get_terminals(inp):
    """
    return terminals where terminals is a dictionnay key = target and value is a
    list of start and end indices
    """
    res = {}
    for row_ind in range(len(inp)):
        for col_ind in range(len(inp[row_ind])):
            current_char = inp[row_ind][col_ind]
            if current_char != "_":
                fields = res.get(current_char)
                if fields :
                    fields.append((col_ind,row_ind))
                else :
                    res[current_char] = (col_ind,row_ind)
    
    return res
                   