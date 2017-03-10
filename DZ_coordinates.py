#coding utf-8


part = None


def coordpart(x, y):

    global part
    if x > 0 and y > 0:
        part = 1

    elif x > 0 and y < 0:
        part = 4

    elif x < 0 and y > 0:
        part = 2

    elif x < 0 and y < 0:
        part = 3

    else:
        part = "Out of parts"

    return part


coordpart(int(input("Введите первое значение (X):")),int(input("Введите второе знаение (Y):")))
print ('Координата находится в части номер {}'.format(part))