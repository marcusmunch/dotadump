# DotaTools
DotaTools is a set of Python scripts that lets you output different information from the OpenDota API to separate files. It requires only little setup (edit details in one(!) file) and no Python skills at all.


### Requirements:

In order to get anything, you must get OpenDota to read your match details. For this, you will need to go into Dota 2's Settings -> Options -> Advanced options -> Social and switch 'Expose Public Match Data' on.

After this, you will need:

- Python (2.7), obviously.
- The Python library BeautifulSoup. Instructions on how to install can be found [here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup).
- ...to log onto OpenDota (regularly*), as it only registers matches played within the last week of your latest login (*: forever if you donate - which you should if you use it so often that this script will be of interest).
- Your Steam32 ID. This is found as a string of numbers in the link to your profile on OpenDota _OR_ your 'Friend ID' on your profile in the Dota 2 client.
- Optional: Access to an FTP server in order to upload your generated file(s).

## How to set up DotaTools
Within the main folder you'll find `settings_example.py`. Edit this file with your FTP logon credentials and your settings and remove the `_example` from the file name, giving you `settings.py`. Remember to turn `DEBUG_MODE` off before you start running your scripts if you actually want it to output files!


Now, as of June 17th 2017, DotaTools contains the following scripts:

- `playedtoday.py` gets a list of your matches played today (after 4AM), including the lobby type (Ranked, Unranked, Solo 1v1 Mid, etc.). (Now that I think of it there might be some bugs. Disregard that for now.)
- `solommr.py` fetches your current Solo MMR as of your latest completed ranked game. If there are no changes to the output file, it will not connect to the FTP server and will not try to upload anything.
- `whattoplay.py` picks a number of heroes (selected by you) from a number of parameters and picks out three random heroes for you to play. Every time this script is run, it will replace the file on the FTP server, as it is currently designed for a single daily run.


Written by [MarcusMunch](http://github.com/MarcusMunch)

Of course, a great big "THANK YOU!" goes out to the guys at [OpenDota](http://www.OpenDota.com) for making the API that's making this whole thing possible! I could literally not have done it without your work! And as I said: Spare them a dollar or five!
