from utils.paths.points import search_around, is_terminals_connect


def refresh_connected_terminals(current_assignment, assignments, connected_terminals, initial_state, inp) -> set:
    """
    input:
    current assignment: {var, value} used to know the current coordinate and color
    to get the adjacent terminals
    assignments: used to check the current points
    connected_terminals: used to get information about the current connected terminals
    initial_state: cached value of first assignment and terminals
    inp: the input matrix

    WARNING:
    This function expects that the current assignment is already consistant so
    any bad combinations will lead to bad results

    result:
    new state of the connected terminals
    """
    current_assignment_coord = list(current_assignment.keys())[0]
    current_assignment_color = current_assignment[current_assignment_coord]


    terminal_connected = is_terminals_connect(
        initial_state, current_assignment_color, inp, assignments)
    if terminal_connected:
        connected_terminals = connected_terminals.copy()
        connected_terminals.add(current_assignment_color.upper())
        return connected_terminals

    return connected_terminals
