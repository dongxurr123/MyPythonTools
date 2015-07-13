__author__ = 'dongxurr123'

import argparse
from xxtea_encrypt import encrypt


def print_usage():
    print("usage: executable -i <src directory, like:D:\\projects\\myQuickGame\\src> -o "
          "<output zip path, like:D:\\game.zip> -k <xxtea key> -s <sign>")


def check_args(args):
    if args.i == None or args.o == None or args.k == None or args.s == None:
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description=u"this tool is use for quick-cocos2d-x 3.3 final version src code encrypt")
    parser.add_argument('-i', help="src file dir")
    parser.add_argument('-o', help="output base dir")
    parser.add_argument('-k', help="xxtea key")
    parser.add_argument('-s', help="sign name")

    args = parser.parse_args();
    if (check_args(args)):
        encrypt(args)
    else:
        print_usage()


if __name__ == "__main__":
    main()