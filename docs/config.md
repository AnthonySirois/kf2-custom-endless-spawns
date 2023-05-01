The `.yaml` config file has three levels:
1. Meta params and global zed spawn params
2. Wave params and wave-specific spawn params
3. Zed params

## Meta parameters
- `mutator_name`: name of the mutator defined at the top of the `.ini` file
- `n_players`: even though the game will automatically adjust a number of zeds depending on the number of players, this might affect zed types ratio or the order in which they spawn; this option, in turn, can provide finer control if you know with how many teammates are you going to play.
- `difficulty`: used to calculate the number of zeds using the data from the [wiki](https://wiki.killingfloor2.com/index.php?title=Endless_Mode)
- `zed_multiplier`: global multiplier of number of all zeds in all waves.
- `custom_zeds_ratio_policy` and `custom_zeds_ratio_policy_params`: Control the ratio of *generated* (i.e. *custom*) zeds, as opposed to zeds generated in KF2 Endless by default.
	- For instance, `custom_zeds_ratio_policy: 'make_line_const_interp'` and `custom_zeds_ratio_policy_params: [[1, 0.975], [20, 0.825]]` will gradually decrease the ratio of *custom* from 97.5% at first wave to 82.5% at 20th, keeping it like that afterward
- `modded`: indicate if modded zeds are included in generation
- `boss_wave_probability`: chance of actually having a boss wave at wave 5, 10, 15, ... 
	- Does not seem to work, but is included nonetheless

## Wave parameters
*Waves do not have to be in order and not all waves have to be defined*
- `num_wave`: wave number
- `name`: custom name for the wave
	- Does not affect the gameplay, but will be included as a comment in the `.ini` file

## Zed parameters
- `zed`: name of the zed
	- If the zeds names are confusing, [zeds docs](./zeds.md) might help
- `ratio`: un-normalized non-negative fraction of certain zed type
- `number`: set amount of the zed to spawn

if both `ratio` and `number` are defined, only `ratio` will be used.

The total number of zeds per wave is estimated from [wiki](https://wiki.killingfloor2.com/index.php?title=Endless_Mode) using meta parameters `n_players` and `difficulty`, after that multiplied by `zed_multiplier`, and finally computed taking into the account `custom_zeds_ratio_policy`, `custom_zeds_ratio_policy_params`.

For boss waves, total zed count is estimated by linearly interpolating between the adjacent waves.

The number of zeds per type using `ratio` is calculated using the total amount per wave, the ratios and numbers of all zeds from the wave. 
- Sum all `number` from the wave's zeds
- Sum all `ratio` from the wave's zed
- `zed_spawn_count` = (`total`  - `sum_number`) * `ratio` / `sum_ratio`


## Spawn parameters
Spawn parameters can be set a every level. The value from the highest level will always be used. For example, if `spawn_at_once` is defined *globally* and at *wave* and *zed* level, the *zed* value will be used. If the *zed*  value was not defined, then it would use the *wave* value...
 - `spawn_at_once`: how many zeds are spawned every spawn attempt
 - `spawn_delay`: how many seconds between each attempt to spawn
 - `probability`: chance of the attempt to spawn to succeed. 0 is 0% (never) and 1 is 100% (always). 
 - `n_generators`: number of "spawners" for certain zed type.
	 - it can be used to spawn zeds more rapidly (e.g. generate all Stalkers in the waves before zeds of all the other types)

 As per [wiki](https://wiki.killingfloor2.com/index.php?title=Endless_Mode), zeds start to spawn faster in later waves, which was actually way too fast for provided set of waves (causing FPS drop); therefore, the multiplication of all `spawn_delay`s the so-called "spawn delay multipliers" is undone (i.e. divided by); this also enables more transparent control of the spawn delays
