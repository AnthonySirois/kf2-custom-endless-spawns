# kf2-hardcore-endless
Configs (A, B) (in YML format) + script to convert to *.ini files (+ ini files themselves).

## Table of contents
* [How to use](#how-to-use)
* [Features](#features)
* [Try these waves!](#try-these-waves)

## How to use
```bash
$ python main.py -h

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

## Features
* can use **all** zeds (including alpha-zeds, bosses, and alpha-Patriarch) available as per May 2018
* KFZedVariant options `spawn_at_once`, `probability`, `spawn_delay`, `number`, and `ratio` can be set
    * globally for all waves and all zeds
    * for specific wave and all zeds
    * for specific wave and specific zed
* `ratio` is (unnormalized) non-negative fraction of certain zed type. Total number of zeds is estimated from [[wiki]](https://wiki.tripwireinteractive.com/index.php?title=Endless_Mode), 
and using meta parameters `n_players` and `difficulty`, after that multiplied by `zed_multiplier`, 
and finally taking into the account `custom_zeds_ratio_policy`, `custom_zeds_ratio_policy_params` which control the
ratio of *generated* (i.e. *custom*) zeds, as opposed to zeds generated in KF2 Endless by default
* for instance, `custom_zeds_ratio_policy: 'make_line_const_interp'` and `custom_zeds_ratio_policy_params: [[1, 0.975], [20, 0.825]]`
will gradually decrease the ratio of *custom* from 97.5% at first wave to 82.5% at 20th, keeping it like that afterwards
* total zed count in boss waves are estimated by linearly interpolating between adjacent waves
* `n_generators` can be used to spawn zeds of certain type more rapidly 
(e.g. generate all of them first during the course of the wave)
* by default, for all zeds, the spawn delay decays too quickly in later waves, according to [[wiki]](https://wiki.tripwireinteractive.com/index.php?title=Endless_Mode);
therefore, all `spawn_delay`s are divided back by spawn delay multipliers, so that they can be controlled more transparently
from the config

See below for examples.

## Try these waves!
* The first config (A) is more hardcore than the second (B) one, and also with more thoroughly designed waves (in terms of zeds combinations, ratios etc.)
* The second config simply contains all possible "special waves" with increasing complexity, that is waves with zeds of same kind only.
* All waves are possible to complete with a decent team. Note the waves which are called "Crawlers" or similar in the config A still contain zeds of various types/subtypes (like Crawler, Elite Crawler, Alpha Crawler).
* ratio (still contain 10-15% of non-custom zeds).

| wave | <div align="center">[config A](config_A/zeds_config.yaml)</div> | <div align="center">[config B](config_B/zeds_config.yaml)</div> |
| :---: | :--- | :--- |
| **1** | "First blood" | Cyst |
| **2** | "2 surprises" | Slasher |
| **3** | Crawler | Crawler |
| **4** | Pondemonium prelude | Clot |
| **5** | **all 4 bosses (T=1min)** | **Abomination** |
| **6** | Bloat | Stalker |
| **7** | "Alpha wave" | Gorefast |
| **8** | Clot | Rioter |
| **9** | Pondemonium | AlphaSlasher |
| **10** | **Hans, 2FPs, Abomination (T=2min)** | **KingFP** |
| **11** | Siren | EliteCrawler |
| **12** | Husk prelude | AlphaHusk |
| **13** | Gorefast | Gorefiend |
| **14** | Pondemonium+ | Siren |
| **15** | **2x King{Flesh, Bloat} bosses (T=3min)** | **Hans** |
| **16** | Bloat + Siren | Bloat |
| **17** | Husk | AlphaStalker |
| **18** | Stalker | AlphaClot |
| **19** | "All of them" | AlphaCrawler |
| **20** | **King Pondemonium (T=4min)** | **AlphaPatriarch** |
| **21** | "Untypical typical wave" | AlphaGorefast |
| **22** | Scrake | Quarterpound |
| **23** | Cyst | AlphaSiren |
| **24** | mini-Pondemonium | AlphaBloat |
| **25** | **King Bloats (T=5min)** | **Patriarch** |
| **26** | Alpha Pondemonium | Scrake |
| **27** | ????? | Husk |
| **28** | ?????[2] | AlphaScrake |
| **29** | &mdash; | AlphaFleshpound |
| **30** | **&mdash;** | **Fleshpound** |
