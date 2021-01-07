from pprint import pprint
def formatter(inp:dict, width, height, init=None):
    pprint(inp)
    res = [[init for i in range(width)] for j in range(height)] 
    for key in inp :
        print('key 1', key[1], 'key 0', key[0])
        res[key[1]][key[0]] = inp[key]

    for i in range(len(res)):
        for j in range(len(res[0])):
            print(res[i][j],end="")
        print()

# testing example
# example = {
# 	(0,0) : 'a',
# 	(0,1) : 'b',
# 	(0,2) : 'c',
# 	(1,0) : 'd',
# 	(1,1) : 'e',
# 	(1,2) : 'f'
# }
# formatter(example,2,3)