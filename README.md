# DotaTools
DotaTools is a set of Python scripts that lets you output different information from the OpenDota API to separate files. It requires only little setup (edit details in one(!) file) and no Python skills at all.

### Requirements:

In order to get anything, you must get OpenDota to read your match details. For this, you will need to go into Dota 2's Settings -> Options -> Advanced options -> Social and switch 'Expose Public Match Data' on.

After this, you will need:

- Python (2.7), obviously.
- ...to log onto OpenDota (regularly*), as it only registers matches played within the last week of your latest login (forever if you donate - it's worth it!).
- Your Steam32 ID. This is found as a string of numbers in the link to your profile on OpenDota _OR_ your 'Friend ID' on your profile in the Dota 2 client.
- Optional: Access to an FTP server in order to upload your generated file(s).

## How to set up DotaTools
Within the main folder you'll find `settings_example.py`. Edit this file with your FTP logon credentials and your settings and remove the `_example` from the file name, giving you `settings.py`.

Now you can run HeroSuggester.py to get an interesting rotation of heroes to your pool!

## To do:

### HeroSuggester.py
- [x] Move API fix from `topHeroes()` to `identifyHeroes()`
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
