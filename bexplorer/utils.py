def formatPrec(n, prec):
    """ 
    Format a value n in terms of an arbitrary precision specifcation value
    """
    return '{0:.{1}f}'.format(prec, n)


def printer(val, hlight):
    """
    Print value in console and highlight type
    """

    highlight = "========= {} =========".format(hlight)
    print highlight
    print val
    print highlight

if __name__ == '__main__':
    print formatPrec(4, 3.1415926535)
    print formatPrec(9, 2.7182818284)
    print formatPrec(0, 100.3)
