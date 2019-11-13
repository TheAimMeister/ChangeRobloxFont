import os
import shutil
from os import listdir, walk

def CustomFontDict():
    onlyfiles = [f for f in listdir(os.getcwd()) if f.endswith('.ttf')]
    return onlyfiles

def GetRobloxVersion():
    rootDict = f'C:/Users/{os.getlogin()}/AppData/Local/Roblox/Versions'
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
        print(f'Creating backup of font: {i}')
        shutil.copy(f'{rootDict}/{i}', f'{os.getcwd()}/OriginalRobloxFont.bak')
    return fonts, rootDict

def ChangeFontsPF():
    CustomFont = CustomFontDict()
    RobloxFont, rootDict = GetFonts()
    for i in RobloxFont:
        if i in CustomFont:
            print(f'Replacing font: {i}')
            shutil.copy(f'{os.getcwd()}/{i}', f'{rootDict}')

ChangeFontsPF()
print('Operation done, press "return" to close')
input()
