#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os.path
import yaml
import zeds
import utility

KF2 = utility.KF2_EndlessUtility


def make_line_interp(x0, y0, x1, y1):
    assert x1 != x0
    def f(x):
        return (y1 - y0) * (x - x0) / (x1 - x0) + y0
    return f


def make_line_const_interp(x0, y0, x1, y1):
    """Same as `make_line_interp`, but extrapolated constantly beyond [x0; x1]."""
    m = min(x0, x1)
    M = max(x0, x1)
    def f(x):
        return make_line_interp(x0, y0, x1, y1)(M if x > M else m if x < m else x)
    return f


class KF2_CustomEndlessWaves(object):
    """Class encapsulating custom zed waves in KF2 Endless mode."""
    @staticmethod
    def default_zed_options():
        return {
            'spawn_at_once': 1,
            'probability': 0.5,
            'spawn_delay': 15.0,
            'ratio': 0.0,
            'number': 0,
            'n_generators': 1
        }

    @staticmethod
    def zed_options():
        return sorted(KF2_CustomEndlessWaves.default_zed_options().keys())
    
    def __init__(self, zeds_config=None):
        self.zeds_config = zeds_config or {}

        # meta parameters
        self.zeds_config.setdefault('n_players', 6)
        self.zeds_config.setdefault('difficulty', 'hoe')
        self.zeds_config.setdefault('zed_multiplier', 1.0)
        self.zeds_config.setdefault('custom_zeds_ratio_policy', lambda n: 1.0)

        # zed specific options
        self.zeds_config.setdefault('zeds_register', [])
        for attr, value in KF2_CustomEndlessWaves.default_zed_options().items():
            self.zeds_config.setdefault(attr, value)

        for attr in self.zeds_config:
            setattr(self, attr, self.zeds_config[attr])

        self.ini_line_template = 'CustomZeds=(Wave={num_wave},SpawnAtOnce={spawn_at_once},Zed="{zed}",'
        self.ini_line_template += 'Probability={probability},Delay={spawn_delay},MaxSpawns={max_zeds})'

    def display(self, markdown=False):
        # collect all names
        names = []
        for zeds_register_wave in self.zeds_register:
            num_wave = zeds_register_wave['num_wave']
            if 'name' in zeds_register_wave:
                names.append((num_wave, zeds_register_wave['name']))
        names.sort()

        # output in the specified format
        if markdown:
            print('| Wave | <div align="center">Name</div> |')
            print('| :---: | :--- |')

        for num_wave, name in names:
            if markdown:
                print('| **{0}** | {1} |'.format(num_wave, name))
            else:
                print('Wave {0}: {1}'.format(num_wave, name))

    def save_ini(self, filename):
        zeds_util = zeds.KF2_ZEDS()

        ini_lines = []
        ini_lines.append('[ZedVarient.ZedVarient]')
        ini_lines.append('ZedMultiplier={0:.6f}'.format(self.zed_multiplier))
        ini_lines.append('bConfigsInit=True')

        for i, zeds_register_wave in enumerate(self.zeds_register):
            # set wave-specific options to the global defaults
            for option in KF2_CustomEndlessWaves.zed_options():
                zeds_register_wave.setdefault(option, self.zeds_config[option])
            
            zeds_register_wave.setdefault('num_wave', i + 1)
            num_wave = zeds_register_wave['num_wave']

            # get or interpolate total number of [all] zeds
            if KF2.is_boss_wave(num_wave):
                n_zeds_f = 0.5 * ( KF2.n_zeds(num_wave - 1, self.n_players, self.difficulty) +
                                   KF2.n_zeds(num_wave + 1, self.n_players, self.difficulty) )
            else:
                n_zeds_f = KF2.n_zeds(num_wave, self.n_players, self.difficulty)
            n_zeds_f *= self.zed_multiplier

            # estimate number of custom zeds
            n_custom_zeds_f = self.custom_zeds_ratio_policy(num_wave) * n_zeds_f

            # preparation loop
            sum_ratio = 0.
            sum_numbers = 0
            for zed_entry in zeds_register_wave['zeds']:

                # set zed-specific options to the wave-specific defaults    
                for option in KF2_CustomEndlessWaves.zed_options():
                    zed_entry.setdefault(option, zeds_register_wave[option])

                # validate params
                zed_entry['spawn_at_once'] = int(zed_entry['spawn_at_once'])
                zed_entry['probability'] = float(zed_entry['probability'])
                zed_entry['spawn_delay'] = float(zed_entry['spawn_delay'])
                zed_entry['number'] = int(zed_entry['number'])
                zed_entry['ratio'] = float(zed_entry['ratio'])
                zed_entry['n_generators'] = int(zed_entry['n_generators'])
                zed_entry['zed'] = zeds_util.zed_alias_to_name(zed_entry['zed'])

                # sum up all ratios and numbers for proper normalization
                sum_ratio += zed_entry['ratio']
                sum_numbers += zed_entry['number']

            # main loop
            for zed_entry in zeds_register_wave['zeds']:

                # compute max number for a particular zed type
                if zed_entry['ratio'] > 0.0:
                    max_zeds_f = (n_custom_zeds_f - sum_numbers) * zed_entry['ratio'] / sum_ratio
                else:
                    max_zeds_f = float(zed_entry['number'])                    
                max_zeds = int(0.5 + max_zeds_f / float(zed_entry['n_generators']))

                # correct `spawn_at_once` if needed
                zed_entry['spawn_at_once'] = min(max_zeds, zed_entry['spawn_at_once'])
                
                # undo multiplication by spawn delay multiplier
                zed_entry['spawn_delay'] *= ( KF2.spawn_delay(zed_entry['spawn_delay'], 1) /
                                              KF2.spawn_delay(zed_entry['spawn_delay'], num_wave) )

                # generate config lines
                for _ in range(zed_entry['n_generators']):
                    s = self.ini_line_template.format(num_wave=num_wave, max_zeds=max_zeds, **zed_entry)
                    ini_lines.append((num_wave, s))

        # sort and produce final string
        ini_lines[3:] = [s for i, s in sorted(ini_lines[3:])]
        s = '\n'.join(ini_lines)

        # save to ini file
        with open(filename, 'w') as f:
            f.write(s + '\n')

        return s


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
