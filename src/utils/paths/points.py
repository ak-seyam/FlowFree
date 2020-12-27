from typing import Tuple
from utils.paths.initial_state import get_initial_state


def get_item_in_coord(mat, coord: Tuple[int, int]):
    # the first [] of mat represents the y axis the second one is the x
    # and current index is tuple of (x,y)
    # that's why i swapped the order in the next line
    return mat[coord[1]][coord[0]]


def is_empty(assignment, coord):
    return assignment.get(coord) == None


def search_around(coord, inp, assignment, search_criteria):
    """
    input:
    coord: the coordinates point of interest 
    inp: 2d list of the input
    search_criteria: function return boolean takes assignments and coordinate respectively

    traverse the four main directions and return all coordinates the meets a specific criteria
    """
    neighbors_coordinates = get_neighbors_coords(coord, inp)
    res = []
    # if coord[0] > 0:  # north
    #     north_coord = (coord[0]-1, coord[1])
    #     if search_criteria(assignment, north_coord):
    #         res.append(north_coord)
    # if coord[0] < len(inp) - 1:  # south
    #     south_coord = (coord[0]+1, coord[1])
    #     if search_criteria(assignment, south_coord):
    #         res.append(south_coord)
    # if coord[1] < len(inp) - 1:  # east
    #     east_coord = (coord[0], coord[1]+1)
    #     if search_criteria(assignment, east_coord):
    #         res.append(east_coord)
    # if coord[1] > 0:  # west
    #     west_coord = (coord[0], coord[1]-1)
    #     if search_criteria(assignment, west_coord):
    #         res.append(west_coord)
    for n_coord in neighbors_coordinates:
        if search_criteria(assignment, n_coord):
            res.append(n_coord)
    return res


def get_neighbors_coords(coord, inp):
    res = []
    if coord[0] > 0:  # north
        res.append((coord[0]-1, coord[1]))
    if coord[0] < len(inp) - 1:  # south
        res.append((coord[0]+1, coord[1]))
    if coord[1] < len(inp) - 1:  # east
        res.append((coord[0], coord[1]+1))
    if coord[1] > 0:  # west
        res.append((coord[0], coord[1]-1))
    return res


def points_are_equal(assignments, point1, point2):
    return (assignments.get(point1) != None) and \
        (assignments.get(point1) == assignments.get(point2))


def get_path(starting_point, end_point, assignments, path, surrounding_equal_points, visited_points, inp):
    """
    use dfs to get the path from starting point by manipulating the path attrib
    """
    if starting_point == None or starting_point in visited_points:
        path.pop()  # remove the last point from path but keep in in the visited points
        return None

    if starting_point == end_point:
        path.append(starting_point)
        return None

    for point in surrounding_equal_points:
        visited_points.append(point)
        path.append(point)
        surrounding_equal_points = search_around(
            point, inp, assignments, lambda assi, p: points_are_equal(assi, p, point))
        get_path(point, inp, end_point, assignments, path,
                 surrounding_equal_points, visited_points)


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
    visited_points = []
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


def check_for_good_combinations(coord, current_color, assignments, inp):
    """
    takes coord and assignments returns true if it is good combination
    """
    # neighbors_coordinates = get_neighbors_coords(coord, inp)
    empty_neighbors = search_around(coord, inp, assignments, is_empty)
    if len(empty_neighbors) >= 2:
        return True

    same_color_neighbors = get_same_color_neighbors(
        coord, current_color, assignments, inp)
    if len(same_color_neighbors) == 2:
        return True

    if len(empty_neighbors) == 1 and len(same_color_neighbors) == 1:
        return True
