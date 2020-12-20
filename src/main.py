from reader.reader import read_inputfile
from utils.paths.non_zigzag_path import is_surrounding_square_filled
from algorithm.backtrack import backtrack
from algorithm import dummy as dum

paths = [
    "../input/input55.txt"
]

inp = read_inputfile(paths[0])
print("input:")
print(inp)

# dummy stuff XD
constraints_dummy = [is_surrounding_square_filled]
res = backtrack(
    constraints_dummy,
    inp,
    dum.select_unassigned_variable,
    dum.order_domain_values,
    dum.assignment_complete,
    dum.inference,
    dum.is_consistant
)

print(res)