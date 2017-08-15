def formatPrec(prec, n):
    """
    Format a value n in terms of an arbitrary precision specifcation value
    """
    prec = int(prec)
    return '{}'.format(n * 10 ** (-prec))


def printer(val, hlight):
    """
    Print value in console and highlight type
    val - value to print
    hlight - title it results or whatever
    """

    highlight = "========= {} =========".format(hlight)
    print(highlight)
    print(val)
    print(highlight)

if __name__ == '__main__':
    print(formatPrec(4, 3.1415926535))
    print(formatPrec(9, 2.7182818284))
    print(formatPrec(0, 100.3))


def save_key(sk, name):
    filename = "{}.pem".format(name)
    with open(filename, "wb") as file:
        file.write(sk)
    return 'name'
