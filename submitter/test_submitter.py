import string
from random import randint
import submitter
import db
import db_initializer


def main():

    db_initializer.main()

    alph = string.ascii_uppercase + string.digits

    flags = []

    for _ in range(10):
        flag = 'ptm'
        for _ in range(28):
            n = randint(0,len(alph)-1)
            flag += alph[n]
        flag += '='
        flags.append(flag)

    for flag in flags:
        db.add_flag(flag, 0)

    submitter.main()

if __name__ == '__main__':
    main()