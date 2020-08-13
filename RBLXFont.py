import shutil, os, logging, sys, time

RblxRootFolder = f'{os.getenv("LOCALAPPDATA")}/Roblox/Versions'
SelfFolder = os.getcwd()
LoggerConfig = logging.basicConfig(filename='Log.log', filemode='w', level=logging.INFO)


#Local Filter Variables
UIPString = """
Multiple fonts found for {0}.
Items found: {1}
Please enter the font you want to keep.
> """

TRESHOLD_LF = 1
DEF_UIP = None


#Functions
def GetRblxExecution():
    global RblxRootFolder

    for (dirpath, dirnames, filenames) in os.walk(RblxRootFolder):
        if "RobloxPlayerBeta.exe" in filenames:
            logging.info(f'Found execution at: {dirpath}')
            RblxRootFolder = f'{dirpath}/content/fonts'
            return

    logging.error('Did not find Roblox execution!')
    sys.exit('Unable to find Roblox execution!')


def FontFilter(LocalFonts):
    new_dict = {}
    userinput = DEF_UIP

    for item, key in LocalFonts.items():
        if len(key) > TRESHOLD_LF:
            userinput = input(UIPString.format(item, key))
        new_dict[item] = userinput or key[0]
        userinput = DEF_UIP

    return new_dict


def getLocalFonts():
    rawlist = os.listdir(SelfFolder)
    LocalFonts = {"semibold": [item for item in rawlist if 'semibold' in item.lower()],
                            "medium": [item for item in rawlist if 'medium' in item.lower()],
                            "regular": [item for item in rawlist if 'regular' in item.lower()],
                            "light": [item for item in rawlist if 'light' in item.lower()],
                            "bold": [item for item in rawlist if 'bold' in item.lower() and not 'semibold' in item.lower()],
                            "italic": [item for item in rawlist if 'italic' in item.lower()]}
    return FontFilter(LocalFonts)


def BackUpRobloxFonts():
    if not os.path.isdir('RobloxDefaultFonts'): os.mkdir('RobloxDefaultFonts')
    AlreadyBackedUp = [f for f in os.listdir(f'{SelfFolder}/RobloxDefaultFonts')]

    for filenames in os.listdir(RblxRootFolder):
        if filenames not in AlreadyBackedUp and not filenames.endswith('.txt'):
            logging.info(f'Creating backup of {filenames} and replacing it.')
            shutil.copy(f'{RblxRootFolder}/{filenames}', f'{SelfFolder}/RobloxDefaultFonts')
            AlreadyBackedUp.append(filenames)


def replaceFonts(LocalFonts):
    rawlist = os.listdir(f'{SelfFolder}/RobloxDefaultFonts')
    localItems = LocalFonts.items()

    for item in rawlist:
        for key, v in localItems:
            if key in item.lower():
                logging.info(f'Replacing font: {item}')
                shutil.copy(f'{SelfFolder}/{v}', f'{RblxRootFolder}/{item}')
                break
        else:
            logging.info(f'Replacing font {item} with the regular font {LocalFonts.get("regular")}')
            shutil.copy(f'{SelfFolder}/{LocalFonts.get("regular")}', f'{RblxRootFolder}/{item}')


delta_start = time.time()
GetRblxExecution()
BackUpRobloxFonts()
replaceFonts(getLocalFonts())
logging.info(f'Operation Done!, took %.2f ms' % (1000*(time.time() - delta_start)))
