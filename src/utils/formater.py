def formatter(inp:dict, width, height, init=None):
    res = [[init for i in range(width)] for j in range(height)] 
    for key in inp :
        res[key[1]][key[0]] = inp[key]

    for i in range(len(res)):
        for j in range(len(res[0])):
            print(res[i][j],end="")
        print()
