# smartest solution
import time
import copy


def read_inputfile(path):
    with open(path) as input_file:
        inp = input_file.read()
        inp = inp.split("\n")
        inp = [list(i) for i in inp]
    return inp

#####################################


######################################

def get_initial_domains(inp):
    h = len(inp)
    w = len(inp[0])
    #domain = [[None for i in range(w)] for j in range(h)]
    domain = {}
    Num_of_domain_values = {}
    domain_levels = [[] for i in range(7)]
    terminals = {}
    is_in_domain = {}
    is_in_terminals = {}

    if inp[0][0] == '_':
        is_in_domain[(0, 0)] = True
        is_in_terminals[(0, 0)] = False
        domain[(0, 0)] = {'┌'}
        Num_of_domain_values[(0, 0)] = 1
        domain_levels[0].append((0, 0))
    else:
        is_in_domain[(0, 0)] = False
        is_in_terminals[(0, 0)] = True
        terminals[(0, 0)] = inp[0][0]

    if inp[h-1][0] == '_':
        is_in_domain[(h-1, 0)] = True
        is_in_terminals[(h-1, 0)] = False
        domain[(h-1, 0)] = {'└'}
        Num_of_domain_values[(h-1, 0)] = 1
        domain_levels[0].append((h-1, 0))
    else:
        terminals[(h-1, 0)] = inp[h-1][0]
        is_in_domain[(h-1, 0)] = False
        is_in_terminals[(h-1, 0)] = True

    if inp[h-1][w-1] == '_':
        is_in_domain[(h-1, w-1)] = True
        is_in_terminals[(h-1, w-1)] = False
        domain[(h-1, w-1)] = {'┘'}
        Num_of_domain_values[(h-1, w-1)] = 1
        domain_levels[0].append((h-1, w-1))
    else:
        terminals[(h-1, w-1)] = inp[h-1][w-1]
        is_in_domain[(h-1, w-1)] = False
        is_in_terminals[(h-1, w-1)] = True

    if inp[0][w-1] == '_':
        is_in_domain[(0, w-1)] = True
        is_in_terminals[(0, w-1)] = False
        domain[(0, w-1)] = {'┐'}
        Num_of_domain_values[(0, w-1)] = 1
        domain_levels[0].append((0, w-1))
    else:
        terminals[(0, w-1)] = inp[0][w-1]
        is_in_domain[(0, w-1)] = False
        is_in_terminals[(0, w-1)] = True

    for i in range(1, w-1):
        if inp[0][i] == '_':
            is_in_domain[(0, i)] = True
            is_in_terminals[(0, i)] = False
            domain[(0, i)] = {'┌', '┐', '─'}
            Num_of_domain_values[(0, i)] = 3
            domain_levels[2].append((0, i))
        else:
            terminals[(0, i)] = inp[0][i]
            is_in_domain[(0, i)] = False
            is_in_terminals[(0, i)] = True

    for i in range(1, h-1):
        if inp[i][0] == '_':
            is_in_domain[(i, 0)] = True
            is_in_terminals[(i, 0)] = False
            domain[(i, 0)] = {'└', '┌', '│'}
            Num_of_domain_values[(i, 0)] = 3
            domain_levels[2].append((i, 0))
        else:
            terminals[(i, 0)] = inp[i][0]
            is_in_domain[(i, 0)] = False
            is_in_terminals[(i, 0)] = True

    for i in range(1, w-1):
        if inp[h-1][i] == '_':
            is_in_domain[(h-1, i)] = True
            is_in_terminals[(h-1, i)] = False
            domain[(h-1, i)] = {'└', '┘', '─'}
            Num_of_domain_values[(h-1, i)] = 3
            domain_levels[2].append((h-1, i))
        else:
            terminals[(w-1, i)] = inp[w-1][i]
            is_in_domain[(w-1, i)] = False
            is_in_terminals[(w-1, i)] = True

    for i in range(1, h-1):
        if inp[i][w-1] == '_':
            is_in_domain[(i, w-1)] = True
            is_in_terminals[(i, w-1)] = False
            domain[(i, w-1)] = {'┐', '┘', '│'}
            Num_of_domain_values[(i, w-1)] = 3
            domain_levels[2].append((i, w-1))
        else:
            terminals[(i, w-1)] = inp[i][w-1]
            is_in_domain[(i, w-1)] = False
            is_in_terminals[(i, w-1)] = True

    for i in range(1, h-1):
        for j in range(1, w-1):
            if inp[i][j] == '_':
                is_in_domain[(i, j)] = True
                is_in_terminals[(i, j)] = False
                domain[(i, j)] = {'└', '┌', '│', '┘', '─', '┐'}
                Num_of_domain_values[(i, j)] = 6
                domain_levels[5].append((i, j))
            else:
                terminals[(i, j)] = inp[i][j]
                is_in_domain[(i, j)] = False
                is_in_terminals[(i, j)] = True

    for i in range(-2, w+2):
        is_in_domain[(-2, i)] = False
        is_in_terminals[(-2, i)] = False

    for i in range(-2, w+2):
        is_in_domain[(-1, i)] = False
        is_in_terminals[(-1, i)] = False

    for i in range(-2, w+2):
        is_in_domain[(h, i)] = False
        is_in_terminals[(h, i)] = False

    for i in range(-2, w+2):
        is_in_domain[(h+1, i)] = False
        is_in_terminals[(h+1, i)] = False

    for i in range(-2, h+2):
        is_in_domain[(i, -2)] = False
        is_in_terminals[(i, -2)] = False

    for i in range(-2, h+2):
        is_in_domain[(i, -1)] = False
        is_in_terminals[(i, -1)] = False

    for i in range(-2, h+2):
        is_in_domain[(i, w)] = False
        is_in_terminals[(i, w)] = False

    for i in range(-2, h+2):
        is_in_domain[(i, w+1)] = False
        is_in_terminals[(i, w+1)] = False

    return domain, Num_of_domain_values, domain_levels, terminals, is_in_domain, is_in_terminals

################################################


#################################################

def reduce_domain(values, location, domains, Num_of_domain_values, domain_levels, assigns):

    if(location in assigns):
        return

    for value in values:
        if(value in domains[location]):
            num = Num_of_domain_values[location]
            domains[location].remove(value)
            domain_levels[num - 1].remove(location)
            domain_levels[num - 2].append(location)
            Num_of_domain_values[location] -= 1

###################################################


###################################################

def eliminate_corners(inp, dir, y, x, domains, Num_of_domain_values, domain_levels, assigns):
    h = len(inp)
    w = len(inp[0])
    length = 0
    if(dir == '┌'):

        length = min(x, y)
        i = y - 1
        j = x - 1

        for k in range(length):
            if(inp[i][j] != '_'):
                break
            reduce_domain([dir], (i, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            i -= 1
            j -= 1
        return

    if(dir == '┘'):
        delta_x = w - (x + 1)
        delta_y = h - (y + 1)
        length = min(delta_x, delta_y)

        i = y + 1
        j = x + 1

        for k in range(length):
            if(inp[i][j] != '_'):
                break
            reduce_domain([dir], (i, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            i += 1
            j += 1

        return

    if(dir == '┐'):
        delta_x = w - (x + 1)
        delta_y = h - (y + 1)
        length = min(delta_x, y)

        i = y - 1
        j = x + 1
        for k in range(length):
            if(inp[i][j] != '_'):
                break
            reduce_domain([dir], (i, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            i -= 1
            j += 1

        return

    if(dir == '└'):
        delta_x = w - (x + 1)
        delta_y = h - (y + 1)

        length = min(x, delta_y)

        i = y + 1
        j = x - 1
        for k in range(length):
            i = y + 1
            j = x - 1
            if(inp[i][j] != '_'):
                break
            reduce_domain([dir], (i, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            i += 1
            j -= 1
    return


##########################################################################################

# initial
def initial_corner_constrains(inp, domains, Num_of_domain_values, domain_levels, is_in_domain):
    h = len(inp)
    w = len(inp[0])
    for i in range(1, w-1):
        #domain[(0, i)] = {'┌', '┐', '─'}
        if(is_in_domain[(0, i)]):
            eliminate_corners(inp, '└', 0, i, domains,
                              Num_of_domain_values, domain_levels, [])
            eliminate_corners(inp, '┘', 0, i, domains,
                              Num_of_domain_values, domain_levels, [])

    for i in range(1, h-1):
        #domain[(i, 0)] = {'└', '┌', '│'}
        if(is_in_domain[(i, 0)]):
            eliminate_corners(inp, '┐', i, 0, domains,
                              Num_of_domain_values, domain_levels, [])
            eliminate_corners(inp, '┘', i, 0, domains,
                              Num_of_domain_values, domain_levels, [])

    for i in range(1, w-1):
        #domain[(w-1, i)] = {'└', '┘', '─'}
        if(is_in_domain[(w-1, i)]):
            eliminate_corners(inp, '┐', w-1, i, domains,
                              Num_of_domain_values, domain_levels, [])
            eliminate_corners(inp, '┌', w-1, i, domains,
                              Num_of_domain_values, domain_levels, [])

    for i in range(1, h-1):
        #domain[(i, h-1)] = {'┐', '┘', '│'}
        if(is_in_domain[(i, w-1)]):
            eliminate_corners(inp, '└', i, w-1, domains,
                              Num_of_domain_values, domain_levels, [])
            eliminate_corners(inp, '┌', i, w-1, domains,
                              Num_of_domain_values, domain_levels, [])


#################################################

def delete_corner(inp, corner_values, location, domains, Num_of_domain_values, domain_levels, assigns):
    for value in corner_values:
        if(value in domains[location]):
            reduce_domain([value], location, domains,
                          Num_of_domain_values, domain_levels, assigns)
            eliminate_corners(
                inp, value, location[0], location[1], domains, Num_of_domain_values, domain_levels, assigns)

#################################################


def reduct_domain(inp, dir, location, domains, Num_of_domain_values, domain_levels, assigns):
    for value in ['└', '┌', '│', '┘', '─', '┐']:
        if(value == dir):
            continue
        if(value != '│' and value != '─'):
            delete_corner(inp, [value], location, domains,
                          Num_of_domain_values, domain_levels, assigns)
        else:
            reduce_domain([value], location, domains,
                          Num_of_domain_values, domain_levels, assigns)

#################################################

# initial


def get_terminals_domain(inp, terminals, domains, Num_of_domain_values, domain_levels, is_in_domain):
    # up =1
    # down = 2
    # right = 3
    # left = 4
    terminal_domain = {}
    for terminal in terminals:
        terminal_domain[(terminal)] = set()
        i = terminal[0]
        j = terminal[1]
        if(is_in_domain[(i-1, j)]):
            terminal_domain[(terminal)].add(1)
        if(is_in_domain[(i+1, j)]):
            terminal_domain[(terminal)].add(2)
        if(is_in_domain[(i, j+1)]):
            terminal_domain[(terminal)].add(3)
        if(is_in_domain[(i, j-1)]):
            terminal_domain[(terminal)].add(4)

        if(len(terminal_domain[terminal]) == 1):
            m = min(terminal_domain[terminal])

            if(m == 1 and is_in_domain[(i-1, j)]):
                delete_corner(inp, ['┘', '└'], (i-1, j), domains,
                              Num_of_domain_values, domain_levels, [])
                reduce_domain(['─'], (i-1, j), domains,
                              Num_of_domain_values, domain_levels, [])

            elif(m == 2 and is_in_domain[(i+1, j)]):
                delete_corner(inp, ['┐', '┌'], (i+1, j), domains,
                              Num_of_domain_values, domain_levels, [])
                reduce_domain(['─'], (i+1, j), domains,
                              Num_of_domain_values, domain_levels, [])

            elif(m == 3 and is_in_domain[(i, j+1)]):
                delete_corner(inp, ['┌', '└'], (i, j+1), domains,
                              Num_of_domain_values, domain_levels, [])
                reduce_domain(['│'], (i, j+1), domains,
                              Num_of_domain_values, domain_levels, [])

            elif(is_in_domain[(i, j-1)]):
                delete_corner(inp, ['┘', '┐'], (i, j-1), domains,
                              Num_of_domain_values, domain_levels, [])
                reduce_domain(['│'], (i, j-1), domains,
                              Num_of_domain_values, domain_levels, [])

    return terminal_domain


#################################################
def reduce_terminals(inp, m, location, terminals, terminal_domain, domains, Num_of_domain_values, domain_levels, assigns):
    terminal_domain[(location)].discard(m)

    i = location[0]
    j = location[1]

    if(len(terminal_domain[location]) == 1):
        m = min(terminal_domain[location])
        if(m == 1):
            delete_corner(inp, ['┘', '└'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)

        elif(m == 2):
            delete_corner(inp, ['┐', '┌'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)

        elif(m == 3):
            delete_corner(inp, ['┌', '└'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        else:
            delete_corner(inp, ['┘', '┐'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)


##################################################

def get_next(dir, location, come_from):
    # up =1
    # down = 2
    # right = 3
    # left = 4
    i = location[0]
    j = location[1]

    if(dir == '└'):
        if(come_from == 1):  # up
            next_ = (i, j+1)  # right
        else:
            next_ = (i-1, j)  # up
    elif(dir == '┌'):
        if(come_from == 2):
            next_ = (i, j+1)  # right
        else:
            next_ = (i+1, j)  # down
    elif(dir == '│'):
        if(come_from == 1):  # up
            next_ = (i+1, j)  # down
        else:
            next_ = (i-1, j)  # up
    elif(dir == '┘'):
        if(come_from == 1):  # up
            next_ = (i, j-1)  # left
        else:
            next_ = (i-1, j)  # up
    elif(dir == '─'):
        if(come_from == 3):  # right
            next_ = (i, j-1)  # left
        else:
            next_ = (i, j+1)  # right
    else:  # '┐'
        if(come_from == 2):  # down
            next_ = (i, j-1)  # left
        else:
            next_ = (i+1, j)  # down
    return next_


######################################################

# initial
def apply_terminals_constrains(inp, terminals, domains, Num_of_domain_values, domain_levels, is_in_domain, is_in_terminals):
    for terminal in terminals:
        i = terminal[0]
        j = terminal[1]

        if((is_in_terminals[(i+2, j)]) and (inp[i+2][j] != inp[i][j]) and is_in_domain[(i+1, j)]):
            reduce_domain(['│'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, [])

        if((is_in_terminals[(i-2, j)]) and (inp[i-2][j] != inp[i][j]) and is_in_domain[(i-1, j)]):
            reduce_domain(['│'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, [])

        if((is_in_terminals[(i, j+2)]) and (inp[i][j+2] != inp[i][j]) and is_in_domain[(i, j+1)]):
            reduce_domain(['─'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, [])

        if((is_in_terminals[(i, j-2)]) and (inp[i][j-2] != inp[i][j]) and is_in_domain[(i, j-1)]):
            reduce_domain(['─'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, [])

        if((is_in_terminals[(i+1, j+1)]) and (inp[i+1][j+1] != inp[i][j])):
            if(is_in_domain[(i, j+1)]):
                delete_corner(inp, ['┐'], (i, j+1), domains,
                              Num_of_domain_values, domain_levels, [])
            if(is_in_domain[(i+1, j)]):
                delete_corner(inp, ['└'], (i+1, j), domains,
                              Num_of_domain_values, domain_levels, [])

        if((is_in_terminals[(i-1, j-1)]) and (inp[i-1][j-1] != inp[i][j])):
            if(is_in_domain[(i, j-1)]):
                delete_corner(inp, ['└'], (i, j-1), domains,
                              Num_of_domain_values, domain_levels, [])
            if(is_in_domain[(i-1, j)]):
                delete_corner(inp, ['┐'], (i-1, j), domains,
                              Num_of_domain_values, domain_levels, [])

        if((is_in_terminals[(i-1, j+1)]) and (inp[i-1][j+1] != inp[i][j])):
            if(is_in_domain[(i, j+1)]):
                delete_corner(inp, ['┘'], (i, j+1), domains,
                              Num_of_domain_values, domain_levels, [])
            if(is_in_domain[(i-1, j)]):
                delete_corner(inp, ['┌'], (i-1, j), domains,
                              Num_of_domain_values, domain_levels, [])

        if((is_in_terminals[(i+1, j-1)]) and (inp[i+1][j-1] != inp[i][j])):
            if(is_in_domain[(i+1, j)]):
                delete_corner(inp, ['┘'], (i+1, j), domains,
                              Num_of_domain_values, domain_levels, [])
            if(is_in_domain[(i, j-1)]):
                delete_corner(inp, ['┌'], (i, j-1), domains,
                              Num_of_domain_values, domain_levels, [])


######################################################

# initial
def reduce_borders_domain(inp, domains, Num_of_domain_values, domain_levels, is_in_domain):
    h = len(inp)
    w = len(inp[0])
    for i in range(1, w-1):
        #domain[(0, i)] = {'┌', '┐', '─'}
        if(is_in_domain[(0, i)]):
            if(is_in_domain[(0, i-1)] and '┌' not in domains[(0, i)]):
                delete_corner(inp, ['┐'], (0, i-1), domains,
                              Num_of_domain_values, domain_levels, [])
            if(is_in_domain[(0, i+1)] and '┐' not in domains[(0, i)]):
                delete_corner(inp, ['┌'], (0, i+1), domains,
                              Num_of_domain_values, domain_levels, [])

    for i in range(1, h-1):
        #domain[(i, 0)] = {'└', '┌', '│'}
        if(is_in_domain[(i, 0)]):
            if(is_in_domain[(i-1, 0)] and '┌' not in domains[(i, 0)]):
                delete_corner(inp, ['└'], (i-1, 0), domains,
                              Num_of_domain_values, domain_levels, [])
            if(is_in_domain[(i+1, 0)] and '└' not in domains[(i, 0)]):
                delete_corner(inp, ['┌'], (i+1, 0), domains,
                              Num_of_domain_values, domain_levels, [])

    for i in range(1, w-1):
        #domain[(w-1, i)] = {'└', '┘', '─'}
        if(is_in_domain[(w-1, i)]):
            if(is_in_domain[(w-1, i-1)] and '└' not in domains[(w-1, i)]):
                delete_corner(inp, ['┘'], (w-1, i-1), domains,
                              Num_of_domain_values, domain_levels, [])
            if(is_in_domain[(w-1, i+1)] and '┘' not in domains[(w-1, i)]):
                delete_corner(inp, ['└'], (w-1, i+1), domains,
                              Num_of_domain_values, domain_levels, [])

    for i in range(1, h-1):
        #domain[(i, h-1)] = {'┐', '┘', '│'}
        if(is_in_domain[(i, h-1)]):
            if(is_in_domain[(i-1, h-1)] and '┐' not in domains[(i, h-1)]):
                delete_corner(inp, ['┘'], (i-1, h-1), domains,
                              Num_of_domain_values, domain_levels, [])
            if(is_in_domain[(i+1, h-1)] and '┘' not in domains[(i, h-1)]):
                delete_corner(inp, ['┐'], (i+1, h-1), domains,
                              Num_of_domain_values, domain_levels, [])


################################################

def color_path(inp, start, source, domains, Num_of_domain_values, domain_levels, assigns, colors, is_in_terminals):
    while(True):
        color = colors[source[0]][source[1]]
        colors[start[0]][start[1]] = color
        dir = assigns[start]
        i, j = source[0] - start[0], source[1] - start[1]

        if(i == -1):
            direc = 1  # up
        elif(i == 1):
            direc = 2  # down
        elif(j == 1):  # right
            direc = 3
        else:  # left
            direc = 4
        _next = get_next(dir, start, direc)
        if(_next not in assigns):
            i = _next[0]
            j = _next[1]
            if(is_in_terminals[(i-1, j)]):
                if(color != colors[i-1][j]):
                    delete_corner(inp, ['┘', '└'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                    reduce_domain(['│'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                elif(color == colors[i-1][j]):
                    delete_corner(inp, ['┐', '┌'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                    reduce_domain(['─'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)

            if(is_in_terminals[(i+1, j)]):
                if(color != colors[i+1][j]):
                    delete_corner(inp, ['┐', '┌'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                    reduce_domain(['│'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                elif(color == colors[i+1][j]):
                    delete_corner(inp, ['┘', '└'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                    reduce_domain(['─'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)

            if(is_in_terminals[(i, j+1)]):
                if(color != colors[i][j+1]):
                    delete_corner(inp, ['┌', '└'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                    reduce_domain(['─'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                elif(color == colors[i][j+1]):
                    delete_corner(inp, ['┘', '┐'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                    reduce_domain(['│'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)

            if(is_in_terminals[(i, j-1)]):
                if(color != colors[i][j-1]):
                    delete_corner(inp, ['┘', '┐'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                    reduce_domain(['─'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                elif(color == colors[i][j-1]):
                    delete_corner(inp, ['┌', '└'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
                    reduce_domain(['│'], (i, j), domains,
                                  Num_of_domain_values, domain_levels, assigns)
            return
        source = start
        start = _next


def reduce_terminals_domain(inp, location, terminal_location, domains, Num_of_domain_values, domain_levels, assigns, is_in_domain):
    i = terminal_location[0]
    j = terminal_location[1]

    if(is_in_domain[(i, j+1)] and (i, j+1) != location):
        delete_corner(inp, ['┘', '┐'], (i, j+1), domains,
                      Num_of_domain_values, domain_levels, assigns)
        reduce_domain(['─'], (i, j+1), domains,
                      Num_of_domain_values, domain_levels, assigns)

    if(is_in_domain[(i, j-1)] and (i, j-1) != location):
        delete_corner(inp, ['└', '┌'], (i, j-1), domains,
                      Num_of_domain_values, domain_levels, assigns)
        reduce_domain(['─'], (i, j-1), domains,
                      Num_of_domain_values, domain_levels, assigns)

    if(is_in_domain[(i-1, j)] and (i-1, j) != location):
        delete_corner(inp, ['┐', '┌'], (i-1, j), domains,
                      Num_of_domain_values, domain_levels, assigns)
        reduce_domain(['│'], (i-1, j), domains,
                      Num_of_domain_values, domain_levels, assigns)

    if(is_in_domain[(i+1, j)] and (i+1, j) != location):
        delete_corner(inp, ['┘', '└'], (i+1, j), domains,
                      Num_of_domain_values, domain_levels, assigns)
        reduce_domain(['│'], (i+1, j), domains,
                      Num_of_domain_values, domain_levels, assigns)


################################################

def Assign(inp, dir, location, terminals, terminal_domain, domains, Num_of_domain_values, domain_levels, assigns, colors, is_in_domain, is_in_terminals):
    i = location[0]
    j = location[1]

    assigns[(i, j)] = dir

    if(dir == '│'):
        # UP
        if(is_in_domain[(i, j+1)]):
            delete_corner(inp, ['┘', '┐'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        elif(is_in_terminals[(i, j+1)]):
            reduce_terminals(inp, 4, (i, j+1), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i, j-1)]):
            delete_corner(inp, ['└', '┌'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i, j-1)]):
            reduce_terminals(inp, 3, (i, j-1), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i+1, j)]):
            delete_corner(inp, ['┌', '┐'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i+1, j)]):
            reduce_terminals_domain(inp, (i, j), (i+1, j), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i-1, j)]):
            delete_corner(inp, ['┘', '└'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)

        elif(is_in_terminals[(i-1, j)]):
            reduce_terminals_domain(inp, (i, j), (i-1, j), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i+1, j+1)]):
            delete_corner(inp, ['┘'], (i+1, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j-1)]):
            delete_corner(inp, ['┌'], (i-1, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i+1, j-1)]):
            delete_corner(inp, ['└'], (i+1, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j+1)]):
            delete_corner(inp, ['┐'], (i-1, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(colors[i-1][j] != '_' and colors[i+1][j] == '_'):
            color_path(inp, (i, j), (i-1, j), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

        elif(colors[i-1][j] == '_' and colors[i+1][j] != '_'):
            color_path(inp, (i, j), (i+1, j), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

    elif(dir == '─'):
        if(is_in_domain[(i, j+1)]):
            delete_corner(inp, ['└', '┌'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i, j+1)]):
            reduce_terminals_domain(inp, (i, j), (i, j+1), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i, j-1)]):
            delete_corner(inp, ['┘', '┐'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i, j-1)]):
            reduce_terminals_domain(inp, (i, j), (i, j-1), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i+1, j)]):
            delete_corner(inp, ['┘', '└'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i+1, j)]):
            reduce_terminals(inp, 1, (i+1, j), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j)]):
            delete_corner(inp, ['┌', '┐'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i-1, j)]):
            reduce_terminals(inp, 2, (i-1, j), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i+1, j+1)]):
            delete_corner(inp, ['┘'], (i+1, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j-1)]):
            delete_corner(inp, ['┌'], (i-1, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i+1, j-1)]):
            delete_corner(inp, ['└'], (i+1, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j+1)]):
            delete_corner(inp, ['┐'], (i-1, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(colors[i][j-1] != '_' and colors[i][j+1] == '_'):
            color_path(inp, (i, j), (i, j-1), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

        elif(colors[i][j-1] == '_' and colors[i][j+1] != '_'):
            color_path(inp, (i, j), (i, j+1), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

    elif(dir == '┌'):
        if(is_in_domain[(i, j+1)]):
            delete_corner(inp, ['└', '┌', '┐'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i, j+1)]):
            reduce_terminals_domain(inp, (i, j), (i, j+1), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i, j-1)]):
            delete_corner(inp, ['└', '┌'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i, j-1)]):
            reduce_terminals(inp, 3, (i, j-1), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i+1, j)]):
            delete_corner(inp, ['└', '┌', '┐'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i+1, j)]):
            reduce_terminals_domain(inp, (i, j), (i+1, j), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i-1, j)]):
            delete_corner(inp, ['┌', '┐'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i-1, j)]):
            reduce_terminals(inp, 2, (i-1, j), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i+1, j+1)]):
            reduce_domain('┘', (i+1, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i+1, j-1)]):
            delete_corner(inp, ['└'], (i+1, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j+1)]):
            delete_corner(inp, ['┐'], (i-1, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(colors[i][j+1] != '_' and colors[i+1][j] == '_'):
            color_path(inp, (i, j), (i, j+1), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

        elif(colors[i][j+1] == '_' and colors[i+1][j] != '_'):
            color_path(inp, (i, j), (i+1, j), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

    elif(dir == '┐'):
        if(is_in_domain[(i, j+1)]):
            delete_corner(inp, ['┘', '┐'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i, j+1)]):
            reduce_terminals(inp, 4, (i, j+1), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i, j-1)]):
            delete_corner(inp, ['┘', '┐', '┌'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i, j-1)]):
            reduce_terminals_domain(inp, (i, j), (i, j-1), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i+1, j)]):
            delete_corner(inp, ['┘', '┐', '┌'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i+1, j)]):
            reduce_terminals_domain(inp, (i, j), (i+1, j), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i-1, j)]):
            delete_corner(inp, ['┌', '┐'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i-1, j)]):
            reduce_terminals(inp, 2, (i-1, j), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i+1, j+1)]):
            delete_corner(inp, ['┘'], (i+1, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j-1)]):
            delete_corner(inp, ['┌'], (i-1, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i+1, j-1)]):
            delete_corner(inp, ['└'], (i+1, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(colors[i][j-1] != '_' and colors[i+1][j] == '_'):
            color_path(inp, (i, j), (i, j-1), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

        elif(colors[i][j-1] == '_' and colors[i+1][j] != '_'):
            color_path(inp, (i, j), (i+1, j), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

    elif(dir == '└'):
        if(is_in_domain[(i, j+1)]):
            delete_corner(inp, ['┘', '└', '┌'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i, j+1)]):
            reduce_terminals_domain(inp, (i, j), (i, j+1), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i, j-1)]):
            delete_corner(inp, ['└', '┌'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i, j-1)]):
            reduce_terminals(inp, 4, (i, j-1), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i+1, j)]):
            delete_corner(inp, ['┘', '└'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i+1, j)]):
            reduce_terminals(inp, 2, (i+1, j), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j)]):
            delete_corner(inp, ['┘', '└', '┌'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i-1, j)]):
            reduce_terminals_domain(inp, (i, j), (i-1, j), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i+1, j+1)]):
            delete_corner(inp, ['┘'], (i+1, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j-1)]):
            delete_corner(inp, ['┌'], (i-1, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j+1)]):
            delete_corner(inp, ['┐'], (i-1, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(colors[i][j+1] != '_' and colors[i-1][j] == '_'):
            color_path(inp, (i, j), (i, j+1), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

        elif(colors[i][j+1] == '_' and colors[i-1][j] != '_'):
            color_path(inp, (i, j), (i-1, j), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

    elif(dir == '┘'):
        if(is_in_domain[(i, j+1)]):
            delete_corner(inp, ['┘', '┐'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i, j+1)]):
            reduce_terminals(inp, 4, (i, j+1), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i, j-1)]):
            delete_corner(inp, ['└', '┘', '┐'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i, j-1)]):
            reduce_terminals_domain(inp, (i, j), (i, j-1), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i+1, j)]):
            delete_corner(inp, ['└', '┘'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['│'], (i+1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i+1, j)]):
            reduce_terminals(inp, 1, (i+1, j), terminals, terminal_domain,
                             domains, Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j)]):
            delete_corner(inp, ['└', '┘', '┐'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
            reduce_domain(['─'], (i-1, j), domains,
                          Num_of_domain_values, domain_levels, assigns)
        elif(is_in_terminals[(i-1, j)]):
            reduce_terminals_domain(inp, (i, j), (i-1, j), domains,
                                    Num_of_domain_values, domain_levels, assigns, is_in_domain)

        if(is_in_domain[(i-1, j-1)]):
            delete_corner(inp, ['┌'], (i-1, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i+1, j-1)]):
            delete_corner(inp, ['└'], (i+1, j-1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(is_in_domain[(i-1, j+1)]):
            delete_corner(inp, ['┐'], (i-1, j+1), domains,
                          Num_of_domain_values, domain_levels, assigns)

        if(colors[i][j-1] != '_' and colors[i-1][j] == '_'):
            color_path(inp, (i, j), (i, j-1), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

        elif(colors[i][j-1] == '_' and colors[i-1][j] != '_'):
            color_path(inp, (i, j), (i-1, j), domains, Num_of_domain_values,
                       domain_levels, assigns, colors, is_in_terminals)

################################################


def get_heuristic(inp, lower_level_domain, domains):
    h = len(inp)
    w = len(inp[0])

    for item in lower_level_domain:
        i = item[0]
        j = item[1]

        dom = domains[item]
        if(i == 0):
            if('┌' in dom):
                return item, '┌'
            else:
                return item, '┐'

        if(i == h-1):
            if('└' in dom):
                return item, '└'
            else:
                return item, '┘'

        if(j == 0):
            if('└' in dom):
                return item, '└'
            else:
                return item, '┌'

        if(j == w-1):
            if('┘' in dom):
                return item, '┘'
            else:
                return item, '┐'

    item = lower_level_domain[0]
    i = item[0]
    j = item[1]
    dom = domains[item]

    if('│' in dom):
        return item, '│'
    elif('─' in dom):
        return item, '─'
    elif('┘' in dom):
        return item, '┘'
    elif('└' in dom):
        return item, '└'
    elif('┌' in dom):
        return item, '┌'
    else:
        return item, '┐'


######################################

def apply_arc_consistency(inp, terminals, terminal_domain, domains, Num_of_domain_values, domain_levels, assigns, colors, is_in_domain, is_in_terminals):

    while(len(domain_levels[0])):

        loc = domain_levels[0].pop(0)
        dire = min(domains[loc])

        Assign(inp, dire, loc, terminals, terminal_domain, domains, Num_of_domain_values,
               domain_levels, assigns, colors, is_in_domain, is_in_terminals)

        if(len(domain_levels[6])):
            return False
    return True


#######################################

def backtrack(inp, terminals, terminal_domain, domains, Num_of_domain_values, domain_levels, assigns, colors, is_in_domain, is_in_terminals):

    if(len(assigns) == len(domains)):
        return assigns

    _terminal_domain = copy.deepcopy(terminal_domain)
    _domains = copy.deepcopy(domains)
    _Num_of_domain_values = copy.deepcopy(Num_of_domain_values)
    _domain_levels = copy.deepcopy(domain_levels)
    _assigns = copy.deepcopy(assigns)
    _colors = copy.deepcopy(colors)

    loc, dire = get_heuristic(inp, _domain_levels[1], _domains)

    _domain_levels[1].remove(loc)

    Assign(inp, dire, loc, terminals, _terminal_domain, _domains, _Num_of_domain_values,
           _domain_levels, _assigns, _colors, is_in_domain, is_in_terminals)
    is_consistant = apply_arc_consistency(inp, terminals, _terminal_domain, _domains,
                                          _Num_of_domain_values, _domain_levels, _assigns, _colors, is_in_domain, is_in_terminals)

    if(is_consistant):
        res = backtrack(inp, terminals, _terminal_domain, _domains, _Num_of_domain_values,
                        _domain_levels, _assigns, _colors, is_in_domain, is_in_terminals)
        if(res != False):
            return res

    domains[loc].remove(dire)
    dire = min(domains[loc])
    domain_levels[1].remove(loc)

    Assign(inp, dire, loc, terminals, terminal_domain, domains, Num_of_domain_values,
           domain_levels, assigns, colors, is_in_domain, is_in_terminals)
    iss_consistant = apply_arc_consistency(inp, terminals, terminal_domain, domains,
                                           Num_of_domain_values, domain_levels, assigns, colors, is_in_domain, is_in_terminals)

    if(iss_consistant):
        _res = backtrack(inp, terminals, terminal_domain, domains, Num_of_domain_values,
                         domain_levels, assigns, colors, is_in_domain, is_in_terminals)
        if(_res != False):
            return _res

    return False


##############################################################

def solve(path):

    inp = read_inputfile(path)

    if(len(inp) == 15):
        inp.pop(14)

    domains, Num_of_domain_values, domain_levels, terminals, is_in_domain, is_in_terminals = get_initial_domains(
        inp)

    print('number of variables: ', len(domains))
    colors = copy.deepcopy(inp)

    initial_corner_constrains(
        inp, domains, Num_of_domain_values, domain_levels, is_in_domain)

    terminal_domain = get_terminals_domain(
        inp, terminals, domains, Num_of_domain_values, domain_levels, is_in_domain)

    apply_terminals_constrains(
        inp, terminals, domains, Num_of_domain_values, domain_levels, is_in_domain, is_in_terminals)

    reduce_borders_domain(inp, domains, Num_of_domain_values,
                          domain_levels, is_in_domain)

    # initial constrains and assignments
    assigns = {}

    while(len(domain_levels[0])):
        loc = domain_levels[0].pop(0)
        dire = min(domains[loc])
        Assign(inp, dire, loc, terminals, terminal_domain, domains, Num_of_domain_values,
               domain_levels, assigns, colors, is_in_domain, is_in_terminals)
        # print(loc, dire)

    Assigns = backtrack(inp, terminals, terminal_domain, domains, Num_of_domain_values,
                        domain_levels, assigns, colors, is_in_domain, is_in_terminals)

    print('\n\nResult: \n')

    resu = inp

    for key in Assigns:
        resu[key[0]][key[1]] = Assigns[key]

    for i in range(len(resu)):
        for j in range(len(resu[0])):
            print(resu[i][j], end="")
        print()

    print('\n')

    print("---------------------------------")

################################################


pathes = [
    '../input/input55.txt',
    '../input/input77.txt',
    '../input/input88.txt',
    '../input/input991.txt',
    '../input/input10101.txt',
    '../input/input10102.txt',
    '../input/input1212.txt',
    '../input/input1214.txt',
    '../input/input1414.txt'
]

for path in pathes:
    start = time.time()
    solve(path)
    print(f'map {path} solution time = {time.time()-start} sec')
