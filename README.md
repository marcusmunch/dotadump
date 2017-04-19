# DotaTools
DotaTools is a set of Python scripts that lets you output different information from the OpenDota API to separate files. It requires only little setup (edit details in one(!) file) and no Python skills at all.

### Requirements:

In order to get anything, you must get OpenDota to read your match details. For this, you will need to go into Dota 2's Settings -> Options -> Advanced options -> Social and switch 'Expose Public Match Data' on.

After this, you will need:

- Python (2.7), obviously.
- ...to log onto OpenDota (regularly*), as it only registers matches played within the last week of your latest login (*: forever if you donate - which you should if you use it so often that this script will be of interest).
- Your Steam32 ID. This is found as a string of numbers in the link to your profile on OpenDota _OR_ your 'Friend ID' on your profile in the Dota 2 client.
- Optional: Access to an FTP server in order to upload your generated file(s).

## How to set up DotaTools
Within the main folder you'll find `settings_example.py`. Edit this file with your FTP logon credentials and your settings and remove the `_example` from the file name, giving you `settings.py`.

Now you can run HeroSuggester.py to get an interesting rotation of heroes to your pool!

## To do:

### HeroSuggester.py
- [ ] Apply minimum winrate for picked heroes

### Setup.py
- [ ] Select minimum winrate for heroes to play in `HeroSuggester.py`

### SoloMMR.py
- [x] Output end time of last ranked game rather than current time

### In general
- [x] Have fun!

Written by MarcusMunch (http://github.com/MarcusMunch)

Of course, a great big "THANK YOU!" goes out to the guys at [OpenDota](http://www.OpenDota.com) for making the API that's making this whole thing possible! I could literally not have done it without your work! And as I said: Spare them a dollar or five!
