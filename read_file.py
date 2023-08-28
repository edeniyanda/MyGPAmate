with open("test.txt", "r")  as fhand:
    fh = fhand.read()
    fh = fh.split("\n")
    print(fh)