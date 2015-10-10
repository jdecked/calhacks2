fname = raw_input("Input the name of your data file: ")

with open(fname, 'rb') as f:
    data = f.read()
