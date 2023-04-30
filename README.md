# kf2-hardcore-endless
This repository contains custom hardcore waves (`ini` files) for Killing Floor 2 Endless mode using [Custom Zed Waves mutator](https://steamcommunity.com/sharedfiles/filedetails/?id=1082749153), as well as a generator of such files from YAML configs with convenient structure. Once you got/generated corresponding `ini` file, see the mutator's docs on how to use it.


## Hardcore endless waves
* config *A* is harder than config *B*
* config *B* simply contain all kinds of so-called _special_ waves (consisting of mostly one zed type), whereas more design thought to create more nasty waves is put into config *A*
* both set of waves can be completed with a decent team, though it might take up to 10 hours depending on your skills
* waves utilize **all** zeds in the game (including alpha-zeds, bosses, and alpha-Patriarch) available as per May 2018
* modded config uses zeds from [Zed Varients](https://steamcommunity.com/sharedfiles/filedetails/?id=938683482) mod
  * It is meant to kill the party and starts trying very hard from wave 16 onward

## How to use the generator
```bash
$ python ./src/main.py -h

usage: main.py [-h] [--txt] [--markdown] PATH

Generate `kfzedvarient.ini` file from given YAML config and save it to the
same directory.

positional arguments:
  PATH        path to YAML config

optional arguments:
  -h, --help  show this help message and exit
  --txt       display wave names (default: False)
  --markdown  display wave names in Markdown format (default: False)
```

For more information on how the config files works, see the 

## Generator features and YAML config structure
* on top of config there are the following meta parameters:
  - `n_players`: even though the game will automatically adjust a number of zeds depending on the number of players, this might affect zed types ratio or the order in which they spawn; this option, in turn, can provide finer control if you know with how many teammates are you going to play
  - `difficulty`: used to calculate the number of zeds from [[wiki]](https://wiki.killingfloor2.com/index.php?title=Endless_Mode)
  - `zed_multiplier`: a global multiplier of number of all zeds in all waves
  - `custom_zeds_ratio_policy` and `custom_zeds_ratio_policy_params`: control the ratio of *generated* (i.e. *custom*) zeds, as opposed to zeds generated in KF2 Endless by default; for instance, `custom_zeds_ratio_policy: 'make_line_const_interp'` and `custom_zeds_ratio_policy_params: [[1, 0.975], [20, 0.825]]`
will gradually decrease the ratio of *custom* from 97.5% at first wave to 82.5% at 20th, keeping it like that afterward
* after that there are zed-specific options, all of which can be set 1) globally for all waves and all zeds, 2) for all zeds in a specific wave, or 3) for specific wave and specific zed:
  - mutator options `spawn_at_once`, `probability`, `spawn_delay`, `number`
  - `ratio`: unnormalized non-negative fraction of certain zed type
  - `n_generators`: number of "spawners" for certain zed type; can be used to spawn zeds more rapidly (e.g. generate all Stalkers in the waves before zeds of all the other types)
* total number of zeds is estimated from [[wiki]](https://wiki.tripwireinteractive.com/index.php?title=Endless_Mode) using meta parameters `n_players` and `difficulty`, after that multiplied by `zed_multiplier`, and finally computed taking into the account `custom_zeds_ratio_policy`, `custom_zeds_ratio_policy_params`
* for boss waves, total zed count is estimated by linearly interpolating between the adjacent waves
* as per [[wiki]](https://wiki.tripwireinteractive.com/index.php?title=Endless_Mode), zeds became to spawn faster in later waves, which was actually way too fast for provided set of waves (causing FPS drop); therefore, the multiplication of all `spawn_delay`s the so-called "spawn delay multipliers" is undone (i.e. divided by); this also enables more transparent control of the spawn delays 