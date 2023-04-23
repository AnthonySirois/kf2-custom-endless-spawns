#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os.path
import yaml
from custom_endless_waves import KF2_CustomEndlessWaves 

def make_line_interp(x0, y0, x1, y1):
    assert x1 != x0
    def f(x):
        return (y1 - y0) * (x - x0) / (x1 - x0) + y0
    return f


def make_line_const_interp(x0, y0, x1, y1):
    """Same as `make_line_interp`, but extrapolated constantly beyond [x0; x1]."""
    min_val = min(x0, x1)
    max_val = max(x0, x1)
    def f(x):
        if(x > max_val): 
            x = max_val
        elif(x < min_val):
            x = min_val

        return make_line_interp(x0, y0, x1, y1)(x)
    return f


def main(args):
    dirpath, _ = os.path.split(args.config_path)
    if not dirpath: dirpath = '.'
    if not dirpath.endswith('/'): dirpath += '/'

    # load config
    with open(args.config_path, 'r') as f:
        try:
            zeds_config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    # validate ratio policy
    f = globals()[zeds_config['custom_zeds_ratio_policy']]
    zeds_config['custom_zeds_ratio_policy'] = f(*zeds_config['custom_zeds_ratio_policy_params'])

    waves = KF2_CustomEndlessWaves(zeds_config)

    # list waves if needed
    if args.txt:
        waves.display()
    elif args.markdown:
        waves.display(markdown=True)

    # generate ini file
    waves.save_ini(os.path.join(dirpath, 'kfzedvarient.ini'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Generate `kfzedvarient.ini` file from given YAML config '
                                                 'and save it to the same directory.')
    parser.add_argument('config_path', metavar='PATH', type=str, help='path to YAML config')
    parser.add_argument('--txt', action='store_true', help='display wave names')
    parser.add_argument('--markdown', action='store_true', help='display wave names in Markdown format')
    args = parser.parse_args()
    main(args)
