import os, shutil, sys, time
from os import listdir, walk

#Prevent from running twice
pidfile = 'ChangeFont.pid'
if os.path.isfile(pidfile):
    print('Already running, exiting')
    time.sleep(2)
    sys.exit(1)

with open(pidfile, 'w') as e:
    e.write(str(os.getpid()))

#Mode definition
PrStr = """
Please type in the mode:
Standard | Standard mode, replaces only the found custom fonts.
All      | Replace all fonts, by duplicating the custom fonts to
           the supported fonts (custom font file must be named 'arial.ttf' without quotes).
           If you want multiple fonts, please put them with the correct file name in CustomFont.bak
Restore  | Restore Roblox's default font.
Exit     | Exit the program.

> """

def requestMode():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        mode = input(PrStr)
        if mode.lower() in ["standard", "all", "restore", "exit"]:
            break
        else:
            print('Enter a valid mode, refreshing screen.')
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
    return mode

#actual code
try:
    def CustomFontDict():
        onlyfiles = [f for f in listdir(os.getcwd()) if f.endswith('.ttf') or f.endswith('.otf')]
        if not os.path.isdir(f'{os.getcwd()}/CustomFont.bak'): os.mkdir('CustomFont.bak')
        if onlyfiles:
            for i in onlyfiles:
                print(f'Moving custom font "{i}" to CustomFont.bak')
                shutil.copy(f'{os.getcwd()}/{i}', f'{os.getcwd()}/CustomFont.bak')
                os.unlink(i)
            else:
                print('Done moving custom font to CustomFont.bak')

    def GetRobloxVersion(mode=False):
        rootDict = f'{os.getenv("LOCALAPPDATA")}/Roblox/Versions'
        for (dirpath, dirnames, filenames) in walk(rootDict):
            if "RobloxPlayerBeta.exe" in filenames:
                rootDict = dirpath
                if not mode:
                    break
                else:
                    rootDict += '/content/fonts'
                    break
        if not mode: print(f'Found Roblox version at:\n{rootDict}')
        return rootDict

    def GetFonts():
        rootDict = f'{GetRobloxVersion()}/content/fonts'
        fonts = [f for f in listdir(rootDict) if f.endswith('.ttf') or f.endswith('.otf')]
        print('Creating backup of original fonts.')
        if not os.path.isdir(f'{os.getcwd()}/OriginalRobloxFont.bak'): os.mkdir('OriginalRobloxFont.bak')
        for i in fonts:
            if i in listdir(f'{os.getcwd()}/OriginalRobloxFont.bak'):
                print(f'Skipping {i}, already backed up.')
                continue
            print(f'Creating backup of font: {i}')
            shutil.copy(f'{rootDict}/{i}', f'{os.getcwd()}/OriginalRobloxFont.bak')
        return fonts, rootDict

    def ChangeFontsPF():
        if modeReturn(requestMode()) == "exit":
            return
        else:
            CustomFont = [f for f in listdir(f'{os.getcwd()}/CustomFont.bak') if f.endswith('.ttf') or f.endswith('otf')]
            RobloxFont, rootDict = GetFonts()
            print("End of backup process")
            for i in RobloxFont:
                if i in CustomFont:
                    print(f'Replacing font: {i}')
                    shutil.copy(f'{os.getcwd()}/CustomFont.bak/{i}', f'{rootDict}')
            else:
                input('Operation done, press "return" to close.')

    def restoreMode():
        print('Initiated restore mode')
        origDict = [f for f in listdir(f'{os.getcwd()}/OriginalRobloxFont.bak') if f.endswith('.ttf') or f.endswith('otf')]
        rootDict = [f for f in listdir(GetRobloxVersion("Restore")) if f.endswith('.ttf') or f.endswith('otf')]
        for i in origDict:
            if i in rootDict:
                print(f'Restoring: {i}')
                shutil.copy(f'{os.getcwd()}/OriginalRobloxFont.bak/{i}', GetRobloxVersion("Restore"))
        return False

    def allMode():
        rootDict = [f for f in listdir(f'{os.getcwd()}/OriginalRobloxFont.bak') if f.endswith('.ttf') or f.endswith('otf')]
        cusFonts = [f for f in listdir(f'{os.getcwd()}/CustomFont.bak') if f.endswith('.ttf') or f.endswith('otf')]
        for i in rootDict:
            if i not in cusFonts:
                print(f'Creating file: {i}')
                shutil.copy(f'{os.getcwd()}/CustomFont.bak/arial.ttf', f'{os.getcwd()}/CustomFont.bak/{i}')
            else:
                print(f'Skipping file: {i}')
        return True

    def modeReturn(mode='standard'):
        if mode.lower() == 'standard':
            return True
        elif mode.lower() == 'all':
            response = allMode()
        elif mode.lower() == 'exit':
            response = mode
        else:
            response = restoreMode()
        return response

    CustomFontDict()
    ChangeFontsPF()
except OSError as e:
    print(f'Error: {e}')
    os.unlink(pidfile)
    sys.exit(1)
finally:
    os.unlink(pidfile)
    sys.exit(0)
