# Clean Start-Cut
Clean-up Start Menu folder. This program moves almost every of your app shortcut to Start Menu from the program’s folder. You can see the icons of your apps instead of their folder.

Currently, if you want to restore every change this program has already done, you only can do it manually. See the "FAQ" section below.

In short:
* *From*: Start Menu >> All Programs >> Program Folder >> Program Shortcut
* *To*: Start Menu >> All Programs >> Program Shortcut

## Python Module
- os
    (probably I would remove this and reimplement with shutil)
- shutil
- ast
- sys
- time
- zipfile
- itertools
- configparser
- fuzzywuzzy (You might want to install it manually)

Install FuzzyWuzzy:

`pip install fuzzywuzzy` or `pip3 install fuzzywuzzy`

Usually, `pip install` on Windows and `pip3 install` on Linux.

## FAQ
Currently, if you want to restore every change this program has already done, you only can do it manually. See the "FAQ" section below.

Q: How can I use this app? Can I double-click that "Clean Start-Cut.py"?
A: I will make the executable later when it is ready for release. For now, you can install [Python 3](https://python.org) and some marked modules listed above manually to try it.

Q: When will it be ready for release?
A: I will announce it on my Instagram and Twitter account, and my blog page. You can find it on the About page on [my blog page here](https://s.id/iketan).

Q: I have already used your program directly on my computer without testing it first, and now I want to restore it. How can I do that?
A: Yes, you can. This program, by default, makes a backup copy as a zip file and stores it on your Desktop. The file name should look like "Start Menu Backup.zip," and you can see the readme.txt file inside it to know where to extract it.

## Changelog
**Note: Some changes very likely to be undocumented**

[v0.5.3]
* Split program name with its version number, and use only the program name for comparison
* Fix for cannot replace the same item name which already exists inside the target folder
* Add folder info inside each backup archive

[v0.5.2]
* Fix for cannot move multiple shortcuts
* Better console output

[v0.5.1]
* Fix auto delete for every folder selected without considering the result of moving the items
* Error fix when a scanned folder has no item to process
* Bug(s):
  * Cannot move multiple shortcut (My mistake, I realize this is a bug)

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
