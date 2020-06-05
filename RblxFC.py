import shutil, os, logging, sys, time

RblxRootFolder = f'{os.getenv("LOCALAPPDATA")}/Roblox/Versions'
SelfFolder = os.getcwd()
LoggerConfig = logging.basicConfig(filename='Log.log', filemode='w', level=logging.INFO)


#Functions
def GetRblxExecution():
    global RblxRootFolder

    for (dirpath, dirnames, filenames) in os.walk(RblxRootFolder):
        if "RobloxPlayerBeta.exe" in filenames:
            logging.info(f'Found execution at: {dirpath}')
            RblxRootFolder = f'{dirpath}/content/fonts'
            return

    logging.error('Did not find Roblox execution')
    sys.exit('Unable to find Roblox execution.')


def waitForFile(item, link):
    while not os.path.isfile(f'{link}/{item}'):
        logging.info(f'Waiting for shutil.copy to complete for {item}')
        time.sleep(.5)


def BackupOriginalFonts():
    if not os.path.isdir('RobloxOriginalFont'): os.mkdir('RobloxOriginalFont')

    logging.info('Trying to retrieve the location')
    alreadyBackedUp = [f for f in os.listdir(f'{SelfFolder}/RobloxOriginalFont')]

    for i in os.listdir(RblxRootFolder):
        if not i.endswith('.txt') and i not in alreadyBackedUp:
            logging.info(f'Backing up file: {i}')
            shutil.copy(f'{RblxRootFolder}/{i}', f'{SelfFolder}/RobloxOriginalFont/{i}')
            waitForFile(i, f'{SelfFolder}/RobloxOriginalFont')
            alreadyBackedUp.append(i)
        else:
            logging.info(f'Skipping file {i}, file is being filtered or already backed up')

    return alreadyBackedUp


def CreateDuplicatesFromArial():
    if not os.path.isfile(f'{os.getcwd()}/arial.ttf' or f'{os.getcwd()}/arial.otf'):
        logging.error('Custom font not found, make sure arial.ttf or arial.otf exists!')
        sys.exit('Custom font not found, make sure arial.ttf or arial.otf exists!')

    if not os.path.isdir('CustomFont'): os.mkdir('CustomFont')

    logging.info('Creating duplicates from arial')
    FontFiles = BackupOriginalFonts()
    AlreadyExisting = [f for f in os.listdir(f'{SelfFolder}/CustomFont')]

    for i in FontFiles:
        if i not in AlreadyExisting:
            logging.info(f'Creating duplicate for {i}')
            shutil.copy(f'{SelfFolder}/arial.ttf' or f'{SelfFolder}/arial.otf',
                        f'{SelfFolder}/CustomFont/{i}')
            waitForFile(i, f'{SelfFolder}/CustomFont')
            AlreadyExisting.append(i)

    return AlreadyExisting


def ReplaceFontAlt(files):
    for i in os.listdir(f'{SelfFolder}/CustomFont'):
        if i in files:
            logging.info(f'Replacing font: {i}')
            shutil.copy(f'SelfFolder/CustomFont/{i}', f'{RblxRootFolder}/{i}')
            waitForFile(i, RblxRootFolder)


def ReplaceRblxFont():
    FilesToReplace = CreateDuplicatesFromArial()
    logging.info(f'Trying to change working directory to:\n{SelfFolder}/CustomFont')

    try: os.chdir(f'{SelfFolder}/CustomFont')
    except:
        logging.error('Failed to change working directory, using alternative method')
        return ReplaceFontAlt(FilesToReplace)

    for i in os.listdir(os.getcwd()):
        if i in FilesToReplace and (i.endswith('.ttf') or i.endswith('.otf')):
            logging.info(f'Replacing file: {i}')
            shutil.copy(f'{os.getcwd()}/{i}', f'{RblxRootFolder}/{i}')
            waitForFile(i, RblxRootFolder)
        else:
            logging.warning(f'Skipping file: {i}')

delta_start = time.time()
GetRblxExecution()
ReplaceRblxFont()
logging.info(f'Operation Done!, took %.2f ms' % (1000*(time.time() - delta_start)))
