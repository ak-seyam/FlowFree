from model.state import state


def backtrack(csp,
              select_unassigned_variable,
              order_domain_values,
              assignment_complete,
              get_inferences,
              is_consistant):
    return _backtrack([], csp, select_unassigned_variable, order_domain_values, assignment_complete, get_inferences, is_consistant)


def _backtrack(assignments: list,
               csp,
               select_unassigned_variable,
               order_domain_values,
               assignment_complete,
               get_inferences,
               is_consistant):
    if assignment_complete(assignments):
        return assignments
    var = select_unassigned_variable(csp)
    for value in order_domain_values():
        if is_consistant({var: value}, assignments, csp):
            assignments.append(value)
            inferences = get_inferences()  # TODO rewrite this after you study consistency
            # TODO check this snippet again
            if inferences != state.failure:
                assignments.extend(inferences)
                res = _backtrack(
                    assignments,
                    csp,
                    select_unassigned_variable,
                    order_domain_values,
                    assignment_complete,
                    get_inferences,
                    is_consistant
                )
            if res != state.failure:
                return res
        # removing failure from assignments doesn't make sense imp
        assignments.remove({var: value})
    return state.failure
