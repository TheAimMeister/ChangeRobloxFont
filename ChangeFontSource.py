import os, shutil, sys, time
from os import listdir, walk

#Prevent from running twice
pidfile = 'ChangeFont.pid'
if os.path.isfile(pidfile):
    print('Already running, exiting')
    time.sleep(2)
    sys.exit(1)

open(pidfile, 'w').write(str(os.getpid()))

#actual code
try:
    def CustomFontDict():
        if not os.path.isdir(f'{os.getcwd()}/CustomFont.bak'):
            os.mkdir('CustomFont.bak')
        onlyfiles = [f for f in listdir(os.getcwd()) if f.endswith('.ttf')]
        if onlyfiles:
            for i in onlyfiles:
                print(i)
                shutil.copy(f'{os.getcwd()}/{i}', f'{os.getcwd()}/CustomFont.bak')
                os.unlink(i)

    def GetRobloxVersion():
        rootDict = f'{os.getenv("LOCALAPPDATA")}/Roblox/Versions'
        for (dirpath, dirnames, filenames) in walk(rootDict):
            if "RobloxPlayerBeta.exe" in filenames:
                rootDict = dirpath
                print(f'Got Roblox Version at: {dirpath}')
                break
        return rootDict

    def GetFonts():
        rootDict = f'{GetRobloxVersion()}/content/fonts'
        fonts = [f for f in listdir(rootDict) if f.endswith('.ttf')]
        print('Creating backup of original fonts.')
        if not os.path.isdir(f'{os.getcwd()}/OriginalRobloxFont.bak'):
            os.mkdir('OriginalRobloxFont.bak')
        for i in fonts:
            if i in listdir(f'{os.getcwd()}/OriginalRobloxFont.bak'):
                print(f'Skipping {i}, already backed up.')
                continue
            print(f'Creating backup of font: {i}')
            shutil.copy(f'{rootDict}/{i}', f'{os.getcwd()}/OriginalRobloxFont.bak')
        return fonts, rootDict

    def ChangeFontsPF():
        CustomFont = [f for f in listdir(f'{os.getcwd()}/CustomFont.bak') if f.endswith('.ttf')]
        print(CustomFont)
        RobloxFont, rootDict = GetFonts()
        for i in RobloxFont:
            if i in CustomFont:
                print(f'Replacing font: {i}')
                shutil.copy(f'{os.getcwd()}/CustomFont.bak/{i}', f'{rootDict}')

    CustomFontDict()
    ChangeFontsPF()
except OSError as e:
    print(f'Error: {e}')
    os.unlink(pidfile)
    sys.exit(1)
finally:
    input('Operation done, press "return" to close.')
    os.unlink(pidfile)
    sys.exit(0)
