def formatPrec(n, value):
    return '{0:.{1}f}'.format(value, n)

if __name__ == '__main__':
    print formatPrec(4, 3.1415926535)
    print formatPrec(9, 2.7182818284)
    print formatPrec(0, 100.3)
