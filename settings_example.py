STEAM_ID = '00000000'  # Your Steam32 ID
FTP_ADDR = 'ftp.domain.com'  # The address for your FTP connection. This will also be used as the username to login. NOTE: If you do not have access to an FTP server, leave this at ''.
FTP_PASS = 'hunter2'  # The password for your FTP connection.

SUGGEST_AMOUNT = 3  # Number of heroes for HeroSuggester.py to suggest
SUGGEST_MIN_DAYS = 30  # Minimum days since you played the heroes picked for HeroSuggester.py
SUGGEST_MIN_GAMES = 10  # Minimum number of games played on heroes picked for HeroSuggester.py
SUGGEST_MIN_WINRATE = 50  # Minimum winrate in percents. NOTE: Due to how Python treats decimals, this doesn't work 100% correctly (may be fixed).

DEBUG_MODE = True  # Set this to False (capital F is important) to begin outputting data
DEBUG_MESSAGE = 'DEBUG MODE ENABLED - NO FILES WILL BE WRITTEN OR OUTPUT'  # You don't HAVE to change this... unless you want a different message in case you debug this yourself.
