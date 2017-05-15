import qrcode
from qrcode.image.pure import PymagingImage
import base64


def formatPrec(n, prec):
    """
    Format a value n in terms of an arbitrary precision specifcation value
    """
    return '{0:.{1}f}'.format(prec, n)


def printer(val, hlight):
    """
    Print value in console and highlight type
    val - value to print
    hlight - title it results or whatever
    """

    highlight = "========= {} =========".format(hlight)
    print highlight
    print val
    print highlight

if __name__ == '__main__':
    print formatPrec(4, 3.1415926535)
    print formatPrec(9, 2.7182818284)
    print formatPrec(0, 100.3)


def make_qrcode(data, name):
    """makes qr codes"""
    img = qrcode.make(data, image_factory=PymagingImage)
    filename = "{}.png".format(name)
    img.save(open(filename, "w+"))

    with open(filename, "rb") as image:
        encoded_img = base64.b64encode(image.read())
    return encoded_img
