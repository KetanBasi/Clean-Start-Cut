import os, ast, re, configparser, itertools, shutil, zipfile, random
from sys import exit as sys_exit

# ANCHOR: Aditional lib
from fuzzywuzzy import fuzz

# ANCHOR: Variables
cfg = configparser.ConfigParser()
cfg.read('config.ini')

inTest = cfg.getboolean('Main', 'inTest')

# Working location
if inTest:
    StartDir = [
        f'{os.getcwd()}\\test_dir\\Start Menu',
        f'{os.getcwd()}\\test_dir\\Start Menu 2'
    ]
else:
    StartDir = [
        "C:\\ProgramData\\Microsoft\\Windows\\Start Menu",
        f"{os.getenv('appdata')}\\Microsoft\\Windows\\Start Menu"
    ]

DBFileName = cfg.get('Main', 'DBFile')
threshold = cfg.getfloat('Main', 'Sensitivity')
maxDepth = cfg.getint('Main', 'MaxDepth')

userHomeDir = os.getenv('userprofile')

filesOnCurrentDir = []

exitStr = [
    'Goodbye!',
    'Bye!',
    'Bye fellas!',
    'See ya later!',
    'Adios!',
    'Ciao!',
    'Have a nice day!'
]

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

Allowed = [
    (Database['Allowed'][program]['FolderName'],
    Database['Allowed'][program]['Target'])
        for
        program in Database['Allowed']
    ]
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
_Unallowed = [
    Database['SysFile']['Directories']] \
    + [
        [Database['Unallowed']['NoGroup'][i]
            for
        i in Database['Unallowed']['NoGroup']]
    ] + [
        Database['Unallowed']['Groups'][j]
            for
        j in Database['Unallowed']['Groups']
    ]
Unallowed = list(set(itertools.chain.from_iterable(_Unallowed)))

# ANCHOR: Functions
def makeDirBackup(pathTarget, dst=f'{userHomeDir}\\Desktop', archiveName='Start Menu Backup'):
    global mainDir
    archiveExtension = '.zip'
    archiveFullName = f'{archiveName}{archiveExtension}'
    print(f'[>>] Backup: {pathTarget} as {archiveFullName}')
    try:
        os.chdir(pathTarget)
        os.chdir('..')
        with zipfile.ZipFile(f'{archiveFullName}', 'w') as zipObj:
            for root, dirs, filenames in os.walk(pathTarget):
                for file in filenames:
                    zipObj.write(
                        os.path.join(root, file),
                        os.path.relpath(
                            os.path.join(root, file),
                            os.path.join(pathTarget, '..')
                        )
                    )
        if os.path.exists(f'{dst}\\{archiveFullName}'):
            fileExsist = True
            i = 1
            while fileExsist:
                if os.path.exists(f'{dst}\\{archiveName} ({i}){archiveExtension}'):
                    i += 1
                else:
                    newArchiveName = f'{archiveName} ({i}){archiveExtension}'
                    print(f'[i ] File exist, save as {newArchiveName} instead')
                    fileExsist = False
                    break
        else:
            newArchiveName = archiveFullName
        shutil.move(archiveFullName, f'{dst}\\{newArchiveName}')
        os.chdir(mainDir)
        print(f'[i ] Backup complete. The backup file moved to {dst}\n')
        return True
    except:
        try: os.remove(archiveName)
        except: pass
        os.chdir(mainDir)
        print(f'[! ] Backup failed')
        return False

def checkAccess(target):
    tempName = '.le-l'
    if type(target) == list:
        if len(target) == 0:
            return False
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
                os.rename(f'{location}/{file}', newName)
            elif not move_up:
                os.rename(file, f'{location}/{newName}')
        except FileExistsError:
            print(f'[! ] Error: File {file} already exist inside target location\n[>>]\tReplacing with the newest one')
            if os.stat(file).st_mtime < os.stat(f'{location}/{newName}').st_mtime and move_up:
                os.rename(f'{location}/{file}', newName)
            elif os.stat(file).st_mtime > os.stat(f'{location}/{newName}').st_mtime and not move_up:
                os.rename(file, f'{location}/{newName}')
        except TypeError:
            return False
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
        print(f'\n\n=== Current Item: {item} ===')
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
                        moveSuccess = moveShortCut(targetList, item, newName=NewItemName)
                        if moveSuccess:
                            shutil.rmtree(item)
                # * Else, ?
                else:
                    os.chdir(item)
                    itemInsideFolder = getFilteredList(getFolder=False)
                    itemFile = findTarget(item, itemInsideFolder)
                    os.chdir('..')
                    moveSuccess = moveShortCut(itemFile, item)
                    if moveSuccess:
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
        print(f'[  ]\tScore A: {score1}\t\tScore B: {score2}')
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

def exitProgram():
    exitMsg = random.choice(exitStr)
    print(f'\n\t{exitMsg}\n')
    sys_exit()

def cleanStartCut(dir):
    global filesOnCurrentDir
    moveWork(dir)
    if not checkAccess('Programs'):
        print(f'''[!!] Error: Cannot work on current directory ({os.getcwd()})
                Please try again with elevated privileges''')
        exitProgram()
    if not filesOnCurrentDir == set():
        moveAll(filesOnCurrentDir, move_up=False)
    moveWork('Programs')
    filesOnCurrentDir = getFilteredList()
    if len(filesOnCurrentDir) == 0:
        print(f'[! ] Nothing to do, everything seems fine.')
    elif not checkAccess(filesOnCurrentDir):
        print(f'''[!!] Error: Cannot work on current directory ({os.getcwd()})
                Please try again with elevated privileges''')
        exitProgram()
    moveAll(filesOnCurrentDir)
    print(f'[i ] Done.')

# ANCHOR: Main
if __name__ == '__main__':
    try:
        needConfirm = True
        while needConfirm:
            for i in range(len(StartDir)):
                print(f'[  ] dir {i + 1}: {StartDir[i]}')
            runConfirm = input('[<<] Confirm: Clean up your Start Menu folder [Y/n] ? ').lower()
            if runConfirm == 'y' or runConfirm == '':
                needConfirm = False
            elif runConfirm == 'n':
                exitProgram()
        mainDir = os.getcwd()
        for startMenuDir in StartDir:
            folderName = startMenuDir.split('\\')[-1]
            os.chdir(f'{startMenuDir}')
            os.chdir(f'..')
            if not makeDirBackup(folderName):
                print(f'''[!!] Error: Cannot make backup.
                        Please try again with elevated privileges''')
                userChoose = True
                while userChoose:
                    print('[??] Would you like to continue without make a backup? [Y/n]')
                    userChoice = input('[<<] Y/n ? ').lower().strip()
                    if userChoice == '' or userChoice == 'y':
                        userChoose = False
                        break
                    elif userChoice == 'n':
                        exitProgram()
                    else:
                        continue
            os.chdir(mainDir)
            cleanStartCut(startMenuDir)
        exitProgram()
    except EOFError or KeyboardInterrupt:
        exitProgram()
