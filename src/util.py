
class RatioPolicies():
    @staticmethod
    def make_line_interp(x0, y0, x1, y1):
        assert x1 != x0
        def f(x):
            return (y1 - y0) * (x - x0) / (x1 - x0) + y0
        return f


    @staticmethod
    def make_line_const_interp(x0, y0, x1, y1):
        """Same as `make_line_interp`, but extrapolated constantly beyond [x0; x1]."""
        min_val = min(x0, x1)
        max_val = max(x0, x1)
        def f(x):
            if(x > max_val): 
                x = max_val
            elif(x < min_val):
                x = min_val

            return RatioPolicies.make_line_interp(x0, y0, x1, y1)(x)
        return f

    @staticmethod
    def constant(x0):
        def f(x):
            return x0
        
        return f

class KF2_EndlessUtility(object):
    """
    Utility class with routines to compute zed count,
    zed count multipliers, spawn rates etc. in KF2 Endless mode.
    Numbers as per 01.05.2018

    References
    ----------
    * https://wiki.tripwireinteractive.com/index.php?title=Endless_Mode
    """
    @staticmethod
    def is_valid_num_wave(num_wave: int) -> bool:
        return isinstance(num_wave, int) and 1 <= num_wave <= 254

    @staticmethod
    def is_valid_n_players(n_players: int) -> bool:
        return isinstance(n_players, int) and 1 <= n_players <= 6

    @staticmethod
    def is_boss_wave(num_wave: int) -> bool:
        return KF2_EndlessUtility.is_valid_num_wave(num_wave) and num_wave % 5 == 0

    @staticmethod
    def __base_zeds_count(num_wave: int) -> int:
        if KF2_EndlessUtility.is_boss_wave(num_wave):
            return 0
        return {1: 25,
                2: 28,
                3: 32,
                4: 32,
                6: 35,
                7: 35,
                8: 35,
                9: 40}.get(num_wave, 42)

    @staticmethod
    def base_zeds_count(num_wave: int) -> int:
        assert KF2_EndlessUtility.is_valid_num_wave(num_wave)
        return KF2_EndlessUtility.__base_zeds_count(num_wave)

    @staticmethod
    def __wave_length_modifier(n_players: int) -> float:
        return {1: 1.0,
                2: 2.0,
                3: 2.75,
                4: 3.5,
                5: 4.0,
                6: 5.0}[n_players]

    @staticmethod
    def wave_length_modifier(n_players: int) -> float:
        assert KF2_EndlessUtility.is_valid_n_players(n_players)
        return KF2_EndlessUtility.__wave_length_modifier(n_players)


    @staticmethod
    def __get_wave_count_mod_table(difficulty: str):
        match difficulty:
            case 'normal':
                return {0: 0.75, 1: 0.8, 2: 0.9, 3: 0.95, 4: 1.0, 5: 1.1} 
            case 'hard':
                return {0: 0.75, 1: 0.8, 2: 0.85, 3: 0.9, 4: 0.95, 5: 1.05} 
            case 'suicidal':
                return {0: 0.75, 1: 0.8, 2: 0.9, 3: 0.95, 4: 0.0, 5: 1.1} 
            case 'hoe':
                return {0: 0.85, 1: 0.9, 2: 0.95, 3: 1.0, 4: 1.05, 5: 1.15}

    @staticmethod
    def __wave_count_mod(num_wave: int, difficulty: str) -> float:
        wave_count_mods = KF2_EndlessUtility.__get_wave_count_mod_table(difficulty)
        if num_wave <= 25:
            return wave_count_mods[(num_wave - 1) // 5]
        return wave_count_mods[5] + 0.1 * ((num_wave - 26) // 5)

    @staticmethod
    def wave_count_mod(num_wave: int, difficulty='hoe') -> float:
        assert KF2_EndlessUtility.is_valid_num_wave(num_wave)
        return KF2_EndlessUtility.__wave_count_mod(num_wave, difficulty)
        
    @staticmethod
    def n_zeds(num_wave: int, n_players: int, difficulty='hoe') -> int:
        x = KF2_EndlessUtility.base_zeds_count(num_wave) *\
            KF2_EndlessUtility.wave_length_modifier(n_players) *\
            KF2_EndlessUtility.wave_count_mod(num_wave, difficulty)
        n = int(x)
        return n

    @staticmethod
    def __get_spawn_rate_modifier_table(difficulty: str):
        match difficulty:
            case 'normal':
                return {0: 0.8, 1: 0.8, 2: 0.7, 3: 0.68, 4: 0.68}
            case 'hard':
                return {0: 0.8, 1: 0.7, 2: 0.68, 3: 0.65, 4: 0.6}
            case 'suicidal':
                return {0: 0.7, 1: 0.68, 2: 0.65, 3: 0.6, 4: 0.55}
            case 'hoe':
                return {0: 0.68, 1: 0.65, 2: 0.6, 3: 0.55, 4: 0.5}

    @staticmethod
    def __spawn_rate_modifier(num_wave: int, difficulty: str) -> float:
        return KF2_EndlessUtility.__get_spawn_rate_modifier_table(difficulty).get(min((num_wave - 1) // 5, 4), 1)

    @staticmethod
    def spawn_delay(base_spawn_delay: float, num_wave: int, difficulty: str) -> float:
        assert base_spawn_delay > 0
        assert KF2_EndlessUtility.is_valid_num_wave(num_wave)
        return max(1, KF2_EndlessUtility.__spawn_rate_modifier(num_wave, difficulty) * base_spawn_delay)