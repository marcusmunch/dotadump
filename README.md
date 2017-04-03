# DotaTools
DotaTools is a set of python scripts that lets you output different information from the OpenDota API to separate files. It requires a config.cfg file that currently needs to be manually generated, but later on there will be a separate script to set up DotaTools for different users etc., since it is intended for automated runs on e.g. a Raspberry Pi.

## To do:

### HeroSuggester.py
- [ ] Move API fix from `topHeroes()` to `identifyHeroes()`
- [x] Print output in one line for better use with AnkhBot
- [x] Upload output to server (maybe separate script for privacy reasons)

### SoloMMR.py
- [ ] Make the file

### Setup.py
- [ ] Select minimum days since `HeroSuggester.py` heroes were last played
- [ ] Select minimum games played with `HeroSuggester.py` heroes
- [ ] Select number of heroes played for `HeroSuggester.py` heroes
- [ ] Select minimum wins for heroes to play in `HeroSuggester.py`

### In general
- [x] Have fun!

Written by MarcusMunch (http://github.com/MarcusMunch)
