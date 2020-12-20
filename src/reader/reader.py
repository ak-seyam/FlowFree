def read_inputfile(path):
    with open(path) as input_file:
        inp = input_file.read()
        inp = inp.split("\n")
        inp = [list(i) for i in inp]
    return inp
