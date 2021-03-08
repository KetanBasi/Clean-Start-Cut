# Clean Start-Cut
Clean-up Start Menu folder so you can run your program a bit faster instead of opening the folder of the program you want to use.

*From*: Start Menu >> All Programs >> Program Folder >> Program Shortcut

*To*: Start Menu >> All Programs >> Program Shortcut


## Python Module
- os
- ast
- configparser
- itertools
- shutil
- sys
- zipfile
- fuzzywuzzy (You might want to install it manually)

Install FuzzyWuzzy:

`pip install fuzzywuzzy` or `pip3 install fuzzywuzzy`

Usually, "pip install" on Windows and "pip3 install" on Linux.

## Changelog

[v0.5.1]
* Fix auto delete for every folder selected without considering the result of moving the items
* Error fix when a scanned folder has no item to process
* Bug(s):
  * Cannot move multiple shortcut

[v0.5]
* Backup Start Menu folder to user Desktop folder

[v0.4.1]
* Check functionality whether directory is accessible for this program. Program stop if the location isn't accessible

[v0.4]
* Rename feature for the known app

[v0.3]
* Use database for known app or name

[v0.2.1]
* Ask user if more than one database file detected

[v0.2]
* Able to use a database file

[v0.1]
* Initial release
