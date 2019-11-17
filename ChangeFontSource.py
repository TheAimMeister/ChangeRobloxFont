import os, shutil, sys, time
from os import listdir, walk

#Prevent from running twice
pidfile = 'ChangeFont.pid'
def is_running():
    try:
        with open(pidfile) as f:
            pid = int(next(f))
        return os.kill(pid, 0)
    except Exception:
        return False

if __name__ == '__main__':
    if is_running():
        print('Program is already running.')
        sys.exit(0)
    with open(pidfile, 'w') as f:
        f.write(f'{os.getpid()}\n')

#Class (might be better for code cleanup, idk...)
class Flander: #Needed a name here, shut.
    CustomFontBak = f'{os.getcwd()}/CustomFont.bak'
    OriginalFontBak = f'{os.getcwd()}/OriginalRobloxFont.bak'
    rootDict = f'{os.getenv("LOCALAPPDATA")}/Roblox/Versions'
    newFiles = [f for f in listdir(os.getcwd()) if f.endswith('.ttf' or '.otf')]

    def __init__(self, mode, otype):
        self.mode = mode
        self.otype = otype
        self.retrieveVersion()
        self.moveCustomFontToBak()
        self.backupOrigF()
        if self.mode and self.otype == "standard":
            self.standardMode()
        elif self.mode and self.otype == "all":
            self.allMode()
            self.standardMode()
        else:
            self.restoreMode()
        return

    def retrieveVersion(self):
        for (dirpath, dirnames, filenames) in walk(self.rootDict):
            if "RobloxPlayerBeta.exe" in filenames:
                self.rootDict = f'{dirpath}/content/fonts'
                break

    def moveCustomFontToBak(self):
        if not os.path.isdir(self.CustomFontBak): os.mkdir('CustomFont.bak')
        if self.newFiles:
            for i in self.newFiles:
                print(f'Moving custom font "{i}" to CustomFont.bak')
                shutil.copy(f'{os.getcwd()}/{i}', self.CustomFontBak)
                os.unlink(i)
            else:
                print('Done moving custom font to CustomFont.bak')

    def backupOrigF(self):
        print("Backup function called for original Roblox fonts")
        if not os.path.isdir(self.OriginalFontBak): os.mkdir('OriginalRobloxFont.bak')
        for i in listdir(self.rootDict):
            if i not in listdir(self.OriginalFontBak) and i.endswith('.ttf' or '.otf'):
                print(f'Creating backup of font: {i}')
                shutil.copy(f'{self.rootDict}/{i}', self.OriginalFontBak)
            else:
                print(f'Skipping {i}, already backed up.')

    def standardMode(self):
        for i in listdir(self.CustomFontBak):
            if i in listdir(self.rootDict):
                print(f'Replacing font: {i}')
                shutil.copy(f'{self.CustomFontBak}/{i}', f'{self.rootDict}')

    def restoreMode(self):
        print('Intiated restore mode')
        for i in listdir(self.OriginalFontBak):
            if i in listdir(self.rootDict):
                print(f'Restoring: {i}')
                shutil.copy(f'{self.OriginalFontBak}/{i}', self.rootDict)

    def allMode(self):
        for i in listdir(self.rootDict):
            if i not in listdir(self.CustomFontBak) and i.endswith('.ttf' or '.otf'):
                print(f'Creating file: {i}')
                shutil.copy(f'{self.CustomFontBak}/arial.ttf', f'{self.CustomFontBak}/{i}')
            else:
                print(f'Skipping file: {i}')

#Input String
PrStr = """
Please type in the mode:
Standard | Standard mode, replaces only the found custom fonts.
All      | Replace all fonts, by duplicating the custom fonts to
           the supported fonts (custom font file must be named 'arial.ttf' without quotes).
           If you want multiple fonts, please put them with the correct file name in CustomFont.bak
Restore  | Restore Roblox's default font.
Exit     | Exit the program.

> """

#call scripts
UIP = ''
while UIP.lower() not in ["standard", "all", "restore", "exit"]:
    os.system('cls' if os.name == 'nt' else 'clear')
    UIP = input(PrStr).lower()

os.system('cls' if os.name == 'nt' else 'clear')
if UIP in ["standard", "all"]:
    Flander(True, UIP)
elif UIP in ["restore"]:
    Flander(False, UIP)
if UIP not in "exit":
    input("Operation done, press 'Return' to close")
os.unlink(pidfile)
sys.exit(0)
