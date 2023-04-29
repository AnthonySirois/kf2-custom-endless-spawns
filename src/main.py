#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os.path
import sys
import yaml
from custom_endless_waves import KF2_CustomEndlessWaves 
from config import ConfigHandler, ValidationError


def main(args):
    dirpath, _ = os.path.split(args.config_path)
    if not dirpath: dirpath = '.'
    if not dirpath.endswith('/'): dirpath += '/'

    with open(args.config_path, 'r') as file:
        try:
            zeds_config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)

    try:
        ConfigHandler.init_config(zeds_config)
    except ValidationError:
        sys.exit("There is an error with the config file")
    except NotImplementedError:
        sys.exit("There is an error with the config file")

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
