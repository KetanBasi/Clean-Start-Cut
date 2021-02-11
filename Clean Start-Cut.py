import os, re, configparser, itertools, shutil

# ANCHOR: Aditional lib
from fuzzywuzzy import fuzz

# ANCHOR: Variables
cfg = configparser.ConfigParser()
cfg.read('config.ini')

# True: use DBSample
# False: use DBFileName to get DB(s)
inTest = cfg.getboolean('Main', 'inTest')

# Working location
if inTest:
    StartDir = cfg.get('Main', 'StartTestDir')
else:
    StartDir = cfg.get('Main', 'StartMenuDir')

DBFileName = cfg.get('Main', 'DBFile')

# TODO: Read database file

threshold = cfg.getfloat('Main', 'Sensitivity')
maxDepth = cfg.getint('Main', 'MaxDepth')

filesOnCurrentDir = []
Database = {

    'Allowed': {
        # ? <Name>: {
        # ?     'FolderName': <Folder name>
        # ?     'Target': <Target(s)>
        # ? }
        'GDrive': {
            'FolderName': 'Backup and Sync from Google',
            'Target': ['Backup and Sync from Google.lnk', 'Google Docs.lnk', 'Google Sheets.lnk', 'Google Slides.lnk']
        },
        'CCleaner': {
            'FolderName': 'CCleaner',
            'Target': ['CCleaner.lnk']
        },
        'Core Temp': {
            'FolderName': 'Core Temp',
            'Target': ['Core Temp.lnk']
        },
        'Dead Cells The Bad Seed': {
            'FolderName': 'Dead Cells The Bad Seed',
            'Target': ['Dead Cells The Bad Seed.lnk']
        },
        'Defraggler': {
            'FolderName': 'Defraggler',
            'Target': ['Defraggler.lnk']
        },
        'Git': {
            'FolderName': 'Git',
            'Target': ['Git Bash.lnk', 'Git CMD.lnk', 'Git GUI.lnk']
        },
        'Glary Utilities 5': {
            'FolderName': 'Glary Utilities 5',
            'Target': ['Glary Utilities 5.lnk']
        },
        'Hard Disk Sentinel': {
            'FolderName': 'Hard Disk Sentinel',
            'Target': ['Hard Disk Sentinel.lnk', 'Hard Disk Sentinel Start Service.lnk', 'Hard Disk Sentinel Stop Service.lnk']
        },
        'IP Camera': {
            'FolderName': 'IP Camera Adapter',
            'Target': ['Configure IP Camera Adapter.lnk']
        },
        'Mendeley': {
            'FolderName': 'Mendeley Desktop',
            'Target': ['Mendeley Desktop.lnk']
        },
        'MongoDB': {
            'FolderName': 'MongoDB',
            'Target': ['MongoDB Compass.lnk']
        },
        'VirtualBox': {
            'FolderName': 'Oracle VM VirtualBox',
            'Target': ['Oracle VM VirtualBox.lnk']
        },
        'Plagiarism Checker X': {
            'FolderName': 'Plagiarism Checker X',
            'Target': ['Launch Plagiarism Checker X.lnk']
        },
        'PowerISO': {
            'FolderName': 'PowerISO',
            'Target': ['PowerISO.lnk', 'PowerISO Virtual Drive Manager.lnk']
        },
        'R': {
            'FolderName': 'R',
            'Target': ['R i386 4.0.3.lnk', 'R x64 4.0.3.lnk']
        },
        'Recuva': {
            'FolderName': 'Recuva',
            'Target': ['Recuva.lnk']
        },
        'Registrar Registry Manager': {
            'FolderName': 'Registrar Registry Manager',
            'Target': ['Registrar Registry Manager.lnk']
        },
        'Revo Uninstaller Pro': {
            'FolderName': 'Revo Uninstaller Pro',
            'Target': ['Revo Uninstaller Pro.lnk']
        },
        'Riot Games': {
            'FolderName': 'Riot Games',
            'Target': ['VALORANT.lnk']
        },
        'RStudio': {
            'FolderName': 'RStudio',
            'Target': ['RStudio.lnk']
        },
        'SafeExamBrowser': {
            'FolderName': 'SafeExamBrowser',
            'Target': ['SEB Configuration Tool.lnk', 'SEB Reset Utility.lnk']
        },
        'SoundWire': {
            'FolderName': 'SoundWire Server',
            'Target': ['SoundWire Server.lnk']
        },
        'Speccy': {
            'FolderName': 'Speccy',
            'Target': ['Speccy.lnk']
        },
        'System Explorer': {
            'FolderName': 'System Explorer',
            'Target': ['System Explorer.lnk']
        },
        'System Tools': {
            'FolderName': 'System Tools',
            'Target': ['Task Manager.lnk']
        },
        'Undeluxe': {
            'FolderName': 'Undeluxe',
            'Target': ['Undeluxe Protected Files Explorer.lnk', 'Undeluxe Control Center.lnk']
        },
        'VcXsrv': {
            'FolderName': 'VcXsrv',
            'Target': ['XLaunch.lnk']
        },
        'Visual Studio Code': {
            'FolderName': 'Visual Studio Code',
            'Target': ['Visual Studio Code.lnk']
        },
        'WhoCrashed': {
            'FolderName': 'WhoCrashed',
            'Target': ['WhoCrashed.lnk']
        },
        'WhySoSlow': {
            'FolderName': 'WhySoSlow',
            'Target': ['WhySoSlow.lnk']
        },
        'WinRAR': {
            'FolderName': 'WinRAR',
            'Target': ['WinRAR.lnk']
        }
    },

    # ? Blacklisted folder so it won't be proceed
    'Unallowed': {
        'NoGroup': {                        # ? <Name>: <Single folder name (ONLY ONE)>
            'WinRAR': 'WinRAR',
            'Office Tools': 'Microsoft Office Tools',
            'Anaconda': 'Anaconda3 (64-bit)',
            'CPUID': 'CPUID',
            'Java': 'Java',
            'Cinema 4D': 'Maxon',
            'Node.js': 'Node.js',
            'Reaper': 'REAPER (x64)',
            'SWI-Prolog 8.2.1': 'SWI-Prolog 8.2.1',
            'USB PC Camera': 'USB PC Camera',
            'VoiceMeeter': 'VB Audio',
            'Virtual Audio Cable': 'Virtual Audio Cable',
            'Visual Studio 2019': 'Visual Studio 2019',
            '': ''
        },
        'Groups': {                         # ? <Name>: <List of folder name(s)>
            # 'AMD': ['AMD Bug Report Tool', 'AMD Radeon Software'],
            'Microsoft': ['Microsoft Office Tools', 'Microsoft Silverlight']
        },
    },

    'SysFile': {                            # ? System Shortcut should be ignored
        'Files': ['desktop.ini', 'config.ini'],           # ? File name must be followed by their extension
        'Directories': [                    # ? Folder name only
            'Accessibility', 'Accessories', 'Administrative Tools', 'Maintenance', 'StartUp',
            'Windows Accessories', 'Windows Administrative Tools', 'Windows Ease of Access',
            'Windows Kits', 'Windows PowerShell', 'Windows System'
        ]
    }
}

conFil = [
    'help',
    'uninstall',
    'homepage',
    'edit',
    'config',
    'eula',
    'faq',
    'readme',
    'release note',
    'website',
    'documentation',
    'visit',
    'license',
    'manual',
    'docs'
]

# ANCHOR: Functions
def moveShortCut(file, location, ext='.lnk', move_up=True):
    try:
        print(f'[>>] Moving: {file}')
        try:
            if file.endswith(ext) and move_up:
                os.rename(f'{location}/{file}', file)
            elif file.endswith(ext) and not move_up:
                os.rename(file, f'{location}/{file}')
        except FileExistsError:
            print(f'[! ] Error: File {file} already exist inside target location\n[>>]\tReplacing with the newest one')
            if os.stat(file).st_mtime < os.stat(f'{location}/{file}').st_mtime and move_up:
                os.rename(f'{location}/{file}', file)
            elif os.stat(file).st_mtime > os.stat(f'{location}/{file}').st_mtime and not move_up:
                os.rename(file, f'{location}/{file}')
        return True
    except FileNotFoundError:
        return False

def moveAll(files, move_up=True):
    if not move_up and os.getcwd().endswith('Start Menu'):
        target = 'Programs'
    elif move_up and '\\Start Menu\\Programs\\' in os.getcwd():
        target = '..'
    else: target = '.'
    for item in files:
        print(f'\n=== Current Item: {item} ===')
        if not move_up:
            moveShortCut(item, location=target, move_up=move_up)
        else:
            try:
                os.chdir(item)
                itemInsideFolder = getFilteredList(getFolder=False)
                itemFile = findTarget(item, itemInsideFolder)
                os.chdir('..')
                moveShortCut(itemFile, item)
                shutil.rmtree(item)
            except NotADirectoryError:
                continue

def findMatch(match, options):
    results = []
    for item in options:
        print(f'[>>] Matching \'{match}\' with \'{item}\'')
        itemName = re.match(r"(.+)[.]{1}[a-zA-Z]+$", item).group(1)
        ratio = fuzz.ratio(match, itemName)
        partialRatio = fuzz.partial_ratio(match, itemName)
        tokenSortRatio = fuzz.token_sort_ratio(match, itemName)
        tokenSetRatio = fuzz.token_set_ratio(match, itemName)
        score1 = 0
        for j in [ratio, partialRatio, tokenSortRatio, tokenSetRatio]:
            if j >= threshold: score1 += 1
        score2 = (ratio + tokenSortRatio) / 2
        results.append( (item, score1, score2) )
        print(f'[  ]\tScore 1: {score1}\t\tScore 2: {score2}')
    score2 = [results[i][2] for i in range(len(results))]
    highest = results[score2.index(max(score2))]
    print(f'[  ]\tScore: {score2}')
    print(f'[>>] Highest:\t{highest[0]}\n[  ]\t\tScore:{highest[2]}')
    return highest[0]

# ! [10/02/2020 0:24AM GMT+7]: Not sure how accurate is this
def findTarget(match, options):
    result = []
    confidence = []
    for i in range(len(options)):
        _result = findMatch(match, options)
        _confidence = 100
        for e in conFil:
            if e in _result.lower():
                _confidence -= len(conFil) + 5
        result.append(_result)
        confidence.append(_confidence)
        print(f'[  ] Score {_confidence}: {_result}')
        if _confidence < confidence[-1]:
            if len(result) > 1 and confidence[-2] < confidence[-1]:
                return result[-1]
            elif len(result) > 1 and confidence[-2] > confidence[-1]:
                return result[-2]
            else:
                confidence.append(_confidence)
                options.remove(_result)
                continue
        else:
            return result[-1]

def getFileFolderList(dir='.'):
    global filesOnCurrentDir
    os.chdir(dir)
    filesOnCurrentDir = os.listdir()
    selectedFiles = [ (Database['Allowed'][program]['FolderName'], Database['Allowed'][program]['Target']) for program in Database['Allowed'] ]
    filterFiles = Database['SysFile']['Files']
    _Unallowed = [Database['SysFile']['Directories']] + [[Database['Unallowed']['NoGroup'][i] for i in Database['Unallowed']['NoGroup']]] + [Database['Unallowed']['Groups'][i] for i in Database['Unallowed']['Groups']]
    Unallowed = list(set(itertools.chain.from_iterable(_Unallowed)))
    try:
        Unallowed.remove('')
    except ValueError:
        pass
    filters = filterFiles + Unallowed + ['Programs']
    _t = set(filesOnCurrentDir) - set(filters)
    return _t

def getFilteredList(getFolder=True):
    _currentFolderList = getFileFolderList()
    result = []
    for item in _currentFolderList:
        try:
            os.chdir(item)
            if getFolder:
                print(item)
                result.append(item)
            os.chdir('..')
        except NotADirectoryError:
            if not getFolder:
                result.append(item)
    return result

def moveWork(target):
    global filesOnCurrentDir
    os.chdir(target)
    filesOnCurrentDir = getFileFolderList()

# ANCHOR: Main
moveWork(StartDir)
if not filesOnCurrentDir == set():
    moveAll(filesOnCurrentDir, move_up=False)

moveWork('Programs')
filesOnCurrentDir = getFilteredList()
print(filesOnCurrentDir)
moveAll(filesOnCurrentDir)

# ANCHOR: =========
