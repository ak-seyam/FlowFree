from typing import Tuple
from utils.paths.initial_state import get_initial_state
import functools


def get_item_in_coord(mat, coord: Tuple[int, int]):
    # the first [] of mat represents the y axis the second one is the x
    # and current index is tuple of (x,y)
    # that's why i swapped the order in the next line
    return mat[coord[1]][coord[0]]


def is_empty(assignment, coord):
    return assignment.get(coord) == None

def is_not_empty(assignment, coord):
    return not is_empty(assignment, coord)

def search_around(coord, inp, assignment, search_criteria):
    """
    input:
    coord: the coordinates point of interest 
    inp: 2d list of the input
    search_criteria: function return boolean takes assignments and coordinate respectively

    traverse the four main directions and return all coordinates the meets a specific criteria
    """
    neighbors_coordinates = get_neighbors_coords(coord,len(inp),len(inp[0]))
    res = []
    for n_coord in neighbors_coordinates:
        if search_criteria(assignment, n_coord):
            res.append(n_coord)
    return res


def get_constrained_nighbours(coord,inp, assignments):
    """
    
    """
    constrained_nighbours = []
    constrained_nighbours += search_around(coord, inp, assignments,is_empty)
    
    neighbors_chain = search_around(coord, inp, assignments,is_not_empty)
    for coord in neighbors_chain:
        constrained_nighbours += search_around(coord, inp, assignments,is_empty)
    
    return constrained_nighbours

@functools.lru_cache(10000)
def get_neighbors_coords(coord,height,width):
    """
    Gives the available neighbors coordinates 

    input: 
        coord: the node of interest coordinates
        inp: the input sample to take information form it
    """
    res = []
    if coord[0] > 0:  # west <-
        res.append((coord[0]-1, coord[1]))
    if coord[0] < width - 1:  # east ->
        res.append((coord[0]+1, coord[1]))
    if coord[1] < height - 1:  # south 🔽
        res.append((coord[0], coord[1]+1))
    if coord[1] > 0:  # north 🔼
        res.append((coord[0], coord[1]-1))
    return res


def points_are_equal(assignments, point1, point2):
    return assignments.get(point1, '').upper() == assignments.get(point2, '').upper()


def get_path(starting_point, end_point, assignments, path, surrounding_equal_points, visited_points, inp):
    """
    use dfs to get the path from starting point by manipulating the path attrib
    """
    if starting_point == None:
        path.pop()  # remove the last point from path but keep in in the visited points
        return None

    if starting_point == end_point:
        path.append(starting_point)
        return None

    for point in surrounding_equal_points:
        if point not in visited_points:
            visited_points.append(point)
            path.append(point)
            surrounding_equal_points = search_around(
                point, inp, assignments, lambda assi, p: points_are_equal(assi, p, point))
            get_path(point, end_point, assignments, path,
                      surrounding_equal_points, visited_points,  inp)


def is_two_points_connected(point1: Tuple[int, int], point2: Tuple[int, int], assignments: dict, inp):
    """
    input:
    point{1,2}: coordinates of the points
    assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals

    return tuple (weather or not the 2 points are connected, path if connected empty otherwise) 
    """
    if assignments.get(point1) == None or assignments.get(point2) == None:
        return False

    if assignments[point1] != assignments[point2]:
        raise Exception("the two point are marked with different values")

    path = [point1]
    visited_points = [point1]
    surrounding_equal_points = search_around(
        point1, inp, assignments, lambda assi, p: points_are_equal(assi, p, point1))
    get_path(point1, point2, assignments, path,
             surrounding_equal_points, visited_points, inp)
    connected = (path[0] == point1) and (path[-1] == point2)
    if not connected:
        path = []
    return connected


def is_terminals_connect(initial_state,terminal_color, inp, assignment):
    terminals = initial_state[0][terminal_color.upper()]
    return is_two_points_connected(terminals[0], terminals[1], assignment, inp)


def get_same_color_neighbors(coord, color, assignments, inp):
    similar_neighbors = search_around(coord, inp, assignments,
                                      lambda assi, point: False if assi.get(point) == None else assi.get(point).lower() == color)
    return similar_neighbors

