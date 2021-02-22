import os, ast, re, configparser, itertools, shutil
from sys import exit as sys_exit

# ANCHOR: Aditional lib
from fuzzywuzzy import fuzz

# ANCHOR: Variables
cfg = configparser.ConfigParser()
cfg.read('config.ini')

inTest = cfg.getboolean('Main', 'inTest')

# Working location
if inTest:
    StartDir = cfg.get('Main', 'StartTestDir')
else:
    StartDir = cfg.get('Main', 'StartMenuDir')

DBFileName = cfg.get('Main', 'DBFile')
threshold = cfg.getfloat('Main', 'Sensitivity')
maxDepth = cfg.getint('Main', 'MaxDepth')

filesOnCurrentDir = []

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

dbFileName = [
    'db',
    'database',
    'db.txt',
    'database.txt'
]

# * Find database file
filesOnCurrentDir = os.listdir()
temp = set(dbFileName).intersection(filesOnCurrentDir)
if len(temp) == 1:
    dbFile = list(temp)[0]
elif len(temp) > 1:
    tempStr = ''.join([f'\n\t{temp.index(i) + 1}. {i}' for i in temp])
    print(f'[!!] Multiple database file detected \
            \n\tPlease select one:\n\t{tempStr}')
    dbSelectInput = int(input("[<<] Select index number: "))
    try:
        dbFile = temp[dbSelectInput - 1]
    except IndexError:
        print('[!!] Invalid input. Should be in range')
else:
    print('''[!!] No database detected
    Database file must be EXACTLY ONE of this list:
    - db\t\t(no extension)
    - database
    - db.txt\t(plaintext extension)
    - database.txt
    If two or more detected, user will be asked to choose one.''')
    exit()


with open(dbFile, 'r') as db:
    Database = ast.literal_eval(db.read())

Allowed = [ (Database['Allowed'][program]['FolderName'], Database['Allowed'][program]['Target']) for program in Database['Allowed'] ]
AllowedFolder = [ item[0] for item in Allowed ]
AllowedTarget = [ item[1] for item in Allowed ]
TargetFolder = []
TargetNewName = []
for item in Database['Allowed']:
    try:
        TargetNewName.append(Database['Allowed'][item]['NewName']) # This first to check if NewName available (<-- private note)
        TargetFolder.append(Database['Allowed'][item]['FolderName'])
    except KeyError:
        continue
filterFiles = Database['SysFile']['Files']
_Unallowed = [Database['SysFile']['Directories']] + [[Database['Unallowed']['NoGroup'][i] for i in Database['Unallowed']['NoGroup']]] + [Database['Unallowed']['Groups'][i] for i in Database['Unallowed']['Groups']]
Unallowed = list(set(itertools.chain.from_iterable(_Unallowed)))

# ANCHOR: Functions
def checkAccess(target):
    tempName = '.le-l'
    if type(target) == list:
        target = target[0]
    if target == tempName:
        tempName = '.leel'
    try:
        os.rename(target, tempName)
        os.rename(tempName, target)
        return True
    except:
        return False

def moveShortCut(file, location, move_up=True, newName=None):
    if newName == None:
        newName = file
    try:
        if newName == None:
            print(f'[>>] Moving: {file}')
        else:
            print(f'[>>] Moving: {file} as \"{newName}\"')
        try:
            if move_up:
                # os.rename(f'{location}/{file}', file)
                os.rename(f'{location}/{file}', newName)
            elif not move_up:
                # os.rename(file, f'{location}/{file}')
                os.rename(file, f'{location}/{newName}')
        except FileExistsError:
            print(f'[! ] Error: File {file} already exist inside target location\n[>>]\tReplacing with the newest one')
            if os.stat(file).st_mtime < os.stat(f'{location}/{newName}').st_mtime and move_up:
                os.rename(f'{location}/{file}', newName)
            elif os.stat(file).st_mtime > os.stat(f'{location}/{newName}').st_mtime and not move_up:
                os.rename(file, f'{location}/{newName}')
        return True
    except FileNotFoundError:
        return False

def moveAll(files, move_up=True, rename=True):
    if not move_up and os.getcwd().endswith('Start Menu'):
        target = 'Programs'
    # ? Useless elif ???
    elif move_up and '\\Start Menu\\Programs\\' in os.getcwd():
        target = '..'
    else: target = '.'
    for item in files:
        print(f'\n=== Current Item: {item} ===')
        if rename and item in TargetFolder:
            NewItemNameList = TargetNewName[TargetFolder.index(item)]
        else:
            NewItemNameList = None
        if not move_up:
            moveShortCut(item, location=target, move_up=move_up, newName=NewItemNameList) # move_up = False (<-- private note)
        else:
            try:
                # * If folder name listed in database (<-- private note)
                if item in AllowedFolder:
                    itemFile = AllowedTarget[AllowedFolder.index(item)]
                    for targetList in itemFile:
                        if NewItemNameList != None:
                            NewItemName = NewItemNameList[itemFile.index(targetList)]
                        else:
                            NewItemName = None
                        moveShortCut(targetList, item, newName=NewItemName)
                # * Else, ?
                else:
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
if not checkAccess('Programs'):
    print(f'''[!!] Error: Cannot work on current directory ({os.getcwd()})
            Please try again with elevated privileges''')
    sys_exit()
if not filesOnCurrentDir == set():
    moveAll(filesOnCurrentDir, move_up=False)

moveWork('Programs')
filesOnCurrentDir = getFilteredList()
if not checkAccess(filesOnCurrentDir):
    print(f'''[!!] Error: Cannot work on current directory ({os.getcwd()})
            Please try again with elevated privileges''')
    sys_exit()
print(filesOnCurrentDir)
moveAll(filesOnCurrentDir)

# ANCHOR: =========
