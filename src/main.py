from reader.reader import read_inputfile
from algorithm.backtrack import backtrack
from algorithm import smart as sm
from algorithm import dummy as dum
from utils.paths.initial_state import get_initial_state
from utils.formater import formatter, formatter
from random import seed

paths = [
    "../input/input88.txt"
]

inp = read_inputfile(paths[0])

initial_state = get_initial_state(inp)

res = backtrack(
    initial_state,
    initial_state[1],
    [],
    inp,
    sm.order_domain_values,
    dum.assignment_complete,
    sm.inference,
    sm.is_consistant,
    lambda assignments: print(assignments), # for testing only
    sm.get_var
)
formatter(res,len(inp),len(inp[0]))
