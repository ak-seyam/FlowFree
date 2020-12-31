from utils.formater import formatter
from model.case import case
from algorithm import smart


def backtrack(
        initial_state,
        initial_assignments,
        inp,
        order_domain_values,
        assignment_complete,
        get_inferences,
        is_consistant,
        callback,
        get_var):
    return _backtrack(initial_state, initial_assignments, inp, order_domain_values, assignment_complete, get_inferences, is_consistant, callback, get_var)


def _backtrack(
        initial_state,
        assignments: dict,
        inp,
        order_domain_values,
        assignment_complete,
        get_inferences,
        is_consistant,
        callback,
        get_var):
    # TODO check if all terminal are connected
    callback(assignments)
    if assignment_complete(assignments, inp):
        return assignments
    v_tuple = get_var(initial_state,assignments,inp)
    if v_tuple == case.failure :
        return case.failure
    var, variables_domain = v_tuple
    # TODO Room for improvement
    if var == None:
        return case.failure
    for value in order_domain_values(initial_state, assignments, inp, var, variables_domain):
        assignments[var] = value
        if is_consistant(initial_state, {var: value},  assignments, inp):
            # print({var: value})
            # formatter(assignments, len(inp), len(inp), init="_")
            # print("-------------------------")
            # return key value for non failure
            inferences = get_inferences()  # TODO rewrite this after you study consistency
            # TODO check this snippet again
            if inferences != case.failure:
                assignments = {**assignments, **inferences}
            res = _backtrack(
                initial_state,
                assignments,
                inp,
                order_domain_values,
                assignment_complete,
                get_inferences,
                is_consistant,
                callback,
                get_var
            )
            if res != case.failure:
                return res
            # IMPORTANT TODO: remove inferences from assignments here (DONE)
            if inferences != case.failure:
                for key in inferences:
                    del assignments[key]

        del assignments[var]
    return case.failure
