from reader.reader import read_inputfile
from algorithm.backtrack import backtrack
from algorithm import dummy as dum
from utils.paths.initial_state import get_initial_state
from utils.formater import formatter, formatter
from random import seed
import time
seed(0)

paths = [
    "../input/input55.txt",
    # "../input/input77.txt",
    # "../input/input88.txt",
    # "../input/input991.txt",
    # "../input/input10101.txt",
    # "../input/input10102.txt",
    # "../input/input1212.txt",
    # "../input/input1214.txt",
    # "../input/input1414.txt",
]
for path in paths:
    inp = read_inputfile(path)
    # print(inp)

    initial_state = get_initial_state(inp)
    # print(initial_state[1])

    # def debug_print(assignments,domain,var,val):
    #     print(f'{var} ,{val}')
    #     print(f'domain {domain[var]}')
    #     formatter(assignments,len(inp[0]), len(inp),init="_")
    c=[0]
    def increase(c,*args):
        c[0]+=1

    start = time.time()
    res = backtrack(
        initial_state,
        initial_state[1],
        inp,
        dum.order_domain_values,
        dum.assignment_complete,
        dum.inference,
        dum.is_consistant,
        lambda *args: increase(c,*args),
        dum.get_var
    )
    print(f'map {path} solution time = {time.time()-start} sec')
    print(f'map {path} number of hits = {c} ')

    formatter(res, len(inp[0]), len(inp))
