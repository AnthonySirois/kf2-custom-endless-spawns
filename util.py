
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
    def _base_zeds_count(num_wave: int) -> int:
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
        return KF2_EndlessUtility._base_zeds_count(num_wave)

    @staticmethod
    def _wave_length_modifier(n_players: int) -> float:
        return {1: 1.0,
                2: 2.0,
                3: 2.75,
                4: 3.5,
                5: 4.0,
                6: 5.0}[n_players]

    @staticmethod
    def wave_length_modifier(n_players: int) -> float:
        assert KF2_EndlessUtility.is_valid_n_players(n_players)
        return KF2_EndlessUtility._wave_length_modifier(n_players)

    @staticmethod
    def _wave_count_mod_hoe(num_wave: int) -> float:
        if num_wave <= 25:
            return {0: 0.85,
                    1: 0.9,
                    2: 0.95,
                    3: 1.0,
                    4: 1.05}[(num_wave - 1) // 5]
        return 1.15 + 0.1 * ((num_wave - 26) // 5)

    @staticmethod
    def wave_count_mod(num_wave: int, difficulty='hoe') -> float:
        assert KF2_EndlessUtility.is_valid_num_wave(num_wave)
        assert difficulty == 'hoe'
        return KF2_EndlessUtility._wave_count_mod_hoe(num_wave)
        
    @staticmethod
    def n_zeds(num_wave: int, n_players: int, difficulty='hoe') -> int:
        x = KF2_EndlessUtility.base_zeds_count(num_wave) *\
            KF2_EndlessUtility.wave_length_modifier(n_players) *\
            KF2_EndlessUtility.wave_count_mod(num_wave, difficulty)
        n = int(x)
        return n

    @staticmethod
    def _spawn_rate_modifier_hoe(num_wave: int) -> float:
        return {0: 0.68,
                1: 0.65,
                2: 0.6,
                3: 0.55,
                4: 0.5,
                5: 0.2}.get((num_wave - 1) // 5, 0)

    @staticmethod
    def spawn_delay(base_spawn_delay: float, num_wave: int) -> float:
        assert base_spawn_delay > 0
        assert KF2_EndlessUtility.is_valid_num_wave(num_wave)
        return max(1, KF2_EndlessUtility._spawn_rate_modifier_hoe(num_wave) * base_spawn_delay)