import shutil, os, time, logging, sys

RblxRootFolder = f'{os.getenv("LOCALAPPDATA")}/Roblox/Versions'
LoggerConfig = logging.basicConfig(filename='RestoreLog.log', filemode='w', level=logging.INFO)


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


def RestoreAlt(old):
    original = [f for f in os.listdir(f'{os.getcwd()}/RobloxOriginalFont')]
    for i in original:
        if i in old and (i.endswith('.ttf') or i.endswith('.otf')):
            logging.info(f'Restoring original font {i}')
            shutil.copy(f'{os.getcwd()}/{i}', f'{RblxRootFolder}/{i}')
            waitForFile(i, RblxRootFolder)
            continue
        else:
            logging.warning(f'File {i} is missing, cannot restore!')


def RestoreFonts():
    rblxFonts = [f for f in os.listdir(RblxRootFolder) if f.endswith('.otf') or f.endswith('.ttf')]

    logging.info(f'Trying to change working directory to {os.getcwd()}/RobloxOriginalFont')
    try: os.chdir(f'{os.getcwd()}/RobloxOriginalFont')
    except:
        logging.warning('Failed to change working directoy, using alternative.')
        RestoreAlt(rblxFonts)

    for i in os.listdir(os.getcwd()):
        if i.endswith('.ttf') or i.endswith('.otf') and i in rblxFonts:
            logging.info(f'Restoring original font {i}')
            shutil.copy(f'{os.getcwd()}/{i}', f'{RblxRootFolder}/{i}')
            waitForFile(i, RblxRootFolder)
            continue
        logging.warning(f'File {i} is missing, cannot restore!')


delta_start = time.time()
GetRblxExecution()
RestoreFonts()
logging.info(f'Operation Done!, took %.2f ms' % (1000*(time.time() - delta_start)))
