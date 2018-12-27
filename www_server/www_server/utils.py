def string_generator():
    str = list("")
    while True:
        length = len(str)
        for i in reversed(range(-1,length)):
            if (i == -1):
                str = list("a") + str
                yield str
                break
            if (str[i] != 'z'):
                str[i] = chr(ord(str[i]) + 1)
                yield str
                break
            elif (str[i] == 'z'):
                str[i] = 'a'