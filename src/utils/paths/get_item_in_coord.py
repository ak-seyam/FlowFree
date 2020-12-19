from typing import Tuple
def get_item_in_coord(mat,coord:Tuple[int,int]):
    # the first [] of mat represents the y axis the second one is the x
    # and current index is tuple of (x,y)
    # that's why i swapped the order in the next line
    return mat[coord[1]][coord[0]]