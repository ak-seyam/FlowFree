from reader.reader import read_inputfile
from algorithm.backtrack import backtrack
from algorithm import dummy as dum
from utils.paths.initial_state import get_initial_state
from utils.formater import formatter, formatter
from random import seed
seed(0)

paths = [
    "../input/input55.txt"
]

inp = read_inputfile(paths[0])

# dummy stuff XD

initial_state = get_initial_state(inp)

res = backtrack(
    initial_state,
    initial_state[1],
    [],
    inp,
    dum.select_unassigned_variable,
    dum.order_domain_values,
    dum.assignment_complete,
    dum.inference,
    dum.is_consistant
)
print(res)
formatter(res,5,5)
