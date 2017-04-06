# DotaTools
DotaTools is a set of python scripts that lets you output different information from the OpenDota API to separate files. It requires a config.cfg file that currently needs to be manually generated, but later on there will be a separate script to set up DotaTools for different users etc., since it is intended for automated runs on e.g. a Raspberry Pi.

## How to set up DotaTools
Within the main folder you'll find `settings_example.py`. Edit this file with your FTP logon credentials and your settings and remove the `_example` from the file name, giving you `settings.py`.

Now you can run HeroSuggester.py to get an interesting rotation of heroes to your pool!

## To do:

### HeroSuggester.py
- [ ] Move API fix from `topHeroes()` to `identifyHeroes()`
- [x] Print output in one line for better use with AnkhBot
- [x] Upload output to server (maybe separate script for privacy reasons)

### SoloMMR.py
- [ ] Make the file

### Setup.py
- [x] Select minimum days since `HeroSuggester.py` heroes were last played
- [x] Select minimum games played with `HeroSuggester.py` heroes
- [x] Select number of heroes played for `HeroSuggester.py` heroes
- [x] Select minimum wins for heroes to play in `HeroSuggester.py`
- [ ] Select minimum winrate for heroes to play in `HeroSuggester.py`

### In general
- [x] Have fun!

Written by MarcusMunch (http://github.com/MarcusMunch)
