


def save_key(sk, name):
    filename = "{}.pem".format(name)
    with open(filename, "wb") as file:
        file.write(sk)
    return 'name'
