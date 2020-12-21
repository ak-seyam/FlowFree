from utils.formater import formatter
from model.case import case


def backtrack(
        initial_assignments,
        csp,
        inp,
        select_unassigned_variable,
        order_domain_values,
        assignment_complete,
        get_inferences,
        is_consistant):
    return _backtrack(initial_assignments, csp, inp, select_unassigned_variable, order_domain_values, assignment_complete, get_inferences, is_consistant)


def _backtrack(assignments: dict,
               csp,
               inp,
               select_unassigned_variable,
               order_domain_values,
               assignment_complete,
               get_inferences,
               is_consistant):
    # TODO check if all terminal are connected
    if assignment_complete(assignments, inp):
        return assignments
    var = select_unassigned_variable(
        csp, assignments, inp)  # TODO Room for improvement
    # TODO Room for improvement
    if var == None:
        return case.failure
    for value in order_domain_values(csp, assignments, inp, var):
        assignments[var] = value
        if is_consistant({var: value},  assignments, inp, csp):
            # print({var: value})
            # formatter(assignments, len(inp), len(inp), init="_")
            # print("-------------------------")
            # return key value for non failure
            inferences = get_inferences()  # TODO rewrite this after you study consistency
            # TODO check this snippet again
            if inferences != case.failure:
                assignments = {**assignments, **inferences}
            res = _backtrack(
                assignments,
                csp,
                inp,
                select_unassigned_variable,
                order_domain_values,
                assignment_complete,
                get_inferences,
                is_consistant
            )
            if res != case.failure:
                return res
            # IMPORTANT TODO: remove inferences from assignments here (DONE)
            if inferences != case.failure:
                for key in inferences:
                    del assignments[key]

        del assignments[var]
    return case.failure
