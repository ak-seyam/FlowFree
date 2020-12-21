from reader.reader import read_inputfile
from utils.paths.non_zigzag_path import is_surrounding_square_filled
from algorithm.backtrack import backtrack
from algorithm import dummy as dum
from utils.paths.initial_state import get_initial_state
from utils.formater import formatter, formatter
from random import seed
seed(42)

paths = [
    "../input/input55.txt"
]

inp = read_inputfile(paths[0])

# dummy stuff XD
constraints_dummy = [is_surrounding_square_filled]
res = backtrack(
    get_initial_state(inp)[1],
    constraints_dummy,
    inp,
    dum.select_unassigned_variable,
    dum.order_domain_values,
    dum.assignment_complete,
    dum.inference,
    dum.is_consistant
)
print(res)
formatter(res,5,5)
