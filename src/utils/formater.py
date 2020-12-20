def to_2d_list(inp:dict, width, height):
    # res = [[None]*width]*height
    res = [[None for i in range(height)] for j in range(width)] 
    for key in inp :
        res[key[1]][key[0]] = inp[key]
    return res

def formatter(twoD_list):
    for i in range(len(twoD_list)):
        for j in range(len(twoD_list[0])):
            print(twoD_list[i][j],end="")
        print()
