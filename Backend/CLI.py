import sys

def extract_args():
    raw_args = sys.argv

    args = []
    kwargs = {}

    for arg in raw_args:
        if '=' in arg:
            arg_split = arg.split('=')
            kwargs[arg_split[0]] = arg_split[1]
        else:
            args.append(arg)

    return args, kwargs