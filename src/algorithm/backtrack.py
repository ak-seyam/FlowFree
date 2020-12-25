from utils.formater import formatter
from model.case import case


def backtrack(
        initial_state,
        initial_assignments,
        csp,
        inp,
        select_unassigned_variable,
        order_domain_values,
        assignment_complete,
        get_inferences,
        is_consistant,
        callback):
    return _backtrack(initial_state, initial_assignments, csp, inp, select_unassigned_variable, order_domain_values, assignment_complete, get_inferences, is_consistant, callback)


def _backtrack(
        initial_state,
        assignments: dict,
        csp,
        inp,
        select_unassigned_variable,
        order_domain_values,
        assignment_complete,
        get_inferences,
        is_consistant,
        callback):
    # TODO check if all terminal are connected
    callback(assignments)
    if assignment_complete(assignments, inp):
        return assignments
    var = select_unassigned_variable(initial_state,
        csp, assignments, inp)  # TODO Room for improvement
    # TODO Room for improvement
    if var == None:
        return case.failure
    for value in order_domain_values(initial_state, csp, assignments, inp, var):
        assignments[var] = value
        if is_consistant(initial_state, {var: value},  assignments, inp, csp):
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
                csp,
                inp,
                select_unassigned_variable,
                order_domain_values,
                assignment_complete,
                get_inferences,
                is_consistant,
                callback
            )
            if res != case.failure:
                return res
            # IMPORTANT TODO: remove inferences from assignments here (DONE)
            if inferences != case.failure:
                for key in inferences:
                    del assignments[key]

        del assignments[var]
    return case.failure
