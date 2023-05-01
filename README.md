# kf2-custom-endless-waves
This repository is a fork of [kf2-hardcore-waves](https://github.com/yell/kf2-hardcore-endless) with added zeds and hopefully an easier code structure to improve/extend if need be.

Like the original repository, it contains custom hardcore waves (`ini` files) for Killing Floor 2 Endless mode using [Custom Zed Waves mutator](https://steamcommunity.com/sharedfiles/filedetails/?id=1082749153), as well as a generator of such files from YAML configs with convenient structure. Once you got/generated corresponding `ini` file, see the mutator's docs on how to use it.


## Hardcore endless waves
* Config *A* is harder than config *B*
* Config *B* simply contain all kinds of so-called _special_ waves (consisting of mostly one zed type), whereas more design thought to create more nasty waves is put into config *A*
* both set of waves can be completed with a decent team, though it might take up to 10 hours depending on your skills
* waves utilize **all** zeds in the game (including alpha-zeds, bosses, and alpha-Patriarch) available as per May 2018
* *Modded* config uses zeds from [Zed Varients](https://steamcommunity.com/sharedfiles/filedetails/?id=938683482) mod
  * It is very unbalanced, but can provide a interesting start to see how the config generation works
  * It is also meant to kill the party and starts trying very hard from wave 16 onward

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

For information on how the config files works, see the [config](./docs/config.md)