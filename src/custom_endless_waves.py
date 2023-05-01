from zeds import KF2_ZEDS
from util import KF2_EndlessUtility

KF2 = KF2_EndlessUtility

class KF2_CustomEndlessWaves(object):    

    def __init__(self, zeds_config=None):
        self.zeds_config = zeds_config or {}

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


    def save_ini(self, filename: str):
        zeds_util = KF2_ZEDS(self.modded)

        ini_lines = []
        ini_lines.append('[{mutator_name}]'.format(mutator_name = self.mutator_name))
        ini_lines.append('ZedMultiplier={0:.6f}'.format(self.zed_multiplier))
        ini_lines.append('bConfigsInit=True')
        
        if self.modded:
            ini_lines.append('bSpawnCustomZeds=True')
            ini_lines.append('OddsOfBossWave={0:.6f}'.format(self.boss_wave_probability))

        n_config_lines = len(ini_lines)

        for zeds_register_wave in self.zeds_register:            
            num_wave = zeds_register_wave['num_wave']

            ini_lines.append((num_wave, ''))
            ini_lines.append((num_wave, ';Wave {0} - {1}'.format(num_wave, zeds_register_wave['name'])))

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
                zed_entry['spawn_delay'] *= ( KF2.spawn_delay(zed_entry['spawn_delay'], 1, self.difficulty) /
                                              KF2.spawn_delay(zed_entry['spawn_delay'], num_wave, self.difficulty))

                #
                # generate config lines
                for _ in range(zed_entry['n_generators']):
                    s = self.ini_line_template.format(num_wave=num_wave, max_zeds=max_zeds, **zed_entry)
                    ini_lines.append((num_wave, s))

        # sort and produce final string
        ini_lines[n_config_lines:] = [s for i, s in sorted(ini_lines[n_config_lines:])]
        s = '\n'.join(ini_lines)

        # save to ini file
        with open(filename, 'w') as file:
            file.write(s + '\n')

        return s