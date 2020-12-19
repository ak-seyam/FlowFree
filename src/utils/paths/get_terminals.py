
def get_terminals(inp):
    """
    return terminals where terminals is a dictionnay key = target and value is a
    list of start and end indices
    """
    
    res = {}
    for row_ind in range(len(inp)):
        for col_ind in range(len(inp[row_ind])):
            current_char = inp[row_ind][col_ind]
            if current_char != "_":
                fields = res.get(current_char)
                if fields :
                    fields.append((col_ind,row_ind))
                else :
                    res[current_char] = (col_ind,row_ind)
    
    return res