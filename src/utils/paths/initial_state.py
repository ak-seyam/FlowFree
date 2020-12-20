
def get_initial_state(inp):
    """
    return tuple of (terminals,initial assignments) where terminals is a dictionnay key = target and value is a
    list of start and end coordinates
    """
    
    terminals = {}
    assignments = {}
    for row_ind in range(len(inp)):
        for col_ind in range(len(inp[row_ind])):
            current_char = inp[row_ind][col_ind]
            if current_char != "_":
                fields = terminals.get(current_char)
                if fields :
                    fields.append((col_ind,row_ind))
                else :
                    terminals[current_char] = [(col_ind,row_ind)]
                assignments[(col_ind,row_ind)] = current_char
    
    return (terminals,assignments)
