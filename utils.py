import argparse


def get_args(params):
    # set parser
    parser = argparse.ArgumentParser()
    # set args
    for arg in params:
        parser.add_argument(arg[0], arg[1], type=arg[2], help=arg[3])

    # parse args
    rec_args = parser.parse_args()
    return rec_args


