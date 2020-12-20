from typing import Tuple
def get_item_in_coord(mat,coord:Tuple[int,int]):
    # the first [] of mat represents the y axis the second one is the x
    # and current index is tuple of (x,y)
    # that's why i swapped the order in the next line
    return mat[coord[1]][coord[0]]

def is_empty(inp,coord):
    return get_item_in_coord(inp,coord) == "_"

def search_around(point,inp,search_criteria):
    """
    input:
    point: the coordinates point of interest 
    inp: 2d list of the input
    search_criteria: function return boolean takes input and coordinate respectively

    traverse the four main directions and return the first coordinate the meets a specific criteria
    """
    if point[0] > 0 : # north
        north_coord = (point[0]-1,point[1])
        if search_criteria(inp,north_coord):
            return north_coord
    if point[0] < len(inp) - 1 : # south 
        south_coord = (point[0]+1,point[1])
        if is_empty(inp,south_coord) :
            return south_coord
    if point[1] < len(inp) - 1 : # east
        east_coord = (point[0],point[1]+1)
        if is_empty(inp,east_coord) :
            return east_coord
    if point[1] > 0 : # west
        west_coord = (point[0],point[1]-1)
        if is_empty(inp,west_coord) :
            return west_coord