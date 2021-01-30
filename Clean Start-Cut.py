import os, sys, configparser, csv, itertools

# ANCHOR: Aditional lib
# try:
#     import ==lib== as ==lib==
# except ModuleNotFoundError:
#     _module = '==lib name=='
#     os.system(f'cmd /c "pip install {_module}"')
#     try:
#         import ==lib== as ==lib==
#     except ModuleNotFoundError:
#         print(f'Module Error: Couldn\'t load install module: {_module}')
#         exit()

# ANCHOR: Variables
cfg = configparser.ConfigParser()
cfg.read('config.ini')

# True: use DBSample
# False: use DBFileName to get DB(s)
inTest = cfg.getboolean('Main', 'inTest')

# Working location
Database = DBSample
if inTest:
    StartDir = cfg.get('Main', 'StartTestDir')
else:
    StartDir = cfg.get('Main', 'StartMenuDir')

DBStyle = cfg.getint('Main', 'DBStyle')
DBFileName = cfg.get('Main', 'DBFile')

if DBStyle == 0:
    with open(DBFileName, 'r') as _DBFile:
        DBFile = _DBFile

# ANCHOR: Functions
def moveShortCut(file, location, ext='.lnk', move_up=True):
    try:
        if file.endswith(ext) and move_up:
            os.rename(f'{location}/{file}', file)
        elif file.endswith(ext) and not move_up:
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
        if not move_up:
            moveShortCut(item, location=target, move_up=move_up)
        else:
            try:
                os.chdir(item)
            except NotADirectoryError:
                continue
            finally:
                print()


# ANCHOR: Main
os.chdir('test_dir/Start Menu')
filesOnCurrentDir = os.listdir()

selectedFiles = [ (Database['Allowed'][program]['FolderName'], Database['Allowed'][program]['Target']) for program in Database['Allowed'] ]
selectedFiles

filterFiles = Database['SysFile']['Files']
_Unallowed = [Database['SysFile']['Directories']] + [[Database['Unallowed']['NoGroup'][i] for i in Database['Unallowed']['NoGroup']]] + [Database['Unallowed']['Groups'][i] for i in Database['Unallowed']['Groups']]
Unallowed = list(set(itertools.chain.from_iterable(_Unallowed)))

filters = set(filterFiles + Unallowed + ['Programs'])

filesOnCurrentDir = set(filesOnCurrentDir) - filters

for item in filesOnCurrentDir:
    if item.endswith('.lnk'):
        os.rename(item, f'Programs/{item}')

moveAll(filesOnCurrentDir, move_up=False)

os.chdir('Programs')


# ANCHOR: =========

if __name__ == '__main__':
    # Something here
    _ = None # ! Dummy line
    DBSample = {

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
                'AMD': ['AMD Bug Report Tool', 'AMD Radeon Software'],
                'Microsoft': ['Microsoft Office Tools', 'Microsoft Silverlight']
            },
        },

        'SysFile': {                            # ? System Shortcut should be ignored
            'Files': ['desktop.ini'],           # ? File name must be followed by their extension
            'Directories': [                    # ? Folder name only
                'Accessibility', 'Accessories', 'Administrative Tools', 'Maintenance', 'Startup',
                'Windows Accessories', 'Windows Administrative Tools', 'Windows Ease of Access',
                'Windows Kits', 'Windows PowerShell', 'Windows System'
            ]
        }

    }
