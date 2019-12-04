import os, shutil, sys, time, asyncio, datetime
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

class Flander():
    CustomFontBak = f'{os.getcwd()}/CustomFont.bak'
    OriginalFontBak = f'{os.getcwd()}/OriginalRobloxFont.bak'
    rootDict = f'{os.getenv("LOCALAPPDATA")}/Roblox/Versions'
    newFiles = [f for f in listdir(os.getcwd()) if f.endswith('.ttf' or '.otf')]

    def __init__(self, mode):
        self.mode = mode
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())
        loop.close()

    async def consoleLog(self, context, type):
        with open('console.txt', 'a+') as f:
            f.write(f'[{datetime.datetime.now()}] {type} | {context}\n')

    async def retrieveVersion(self):
        for (dirpath, dirnames, filenames) in walk(self.rootDict):
            if "RobloxPlayerBeta.exe" in filenames:
                await self.consoleLog(f'Found version at: {dirpath}', 'OPERATION')
                self.rootDict = f'{dirpath}/content/fonts'
                break

    async def moveCustomFontToBak(self):
        if not os.path.isdir(self.CustomFontBak): os.mkdir('CustomFont.bak')
        if self.newFiles:
            for i in self.newFiles:
                shutil.copy(f'{os.getcwd()}/{i}', self.CustomFontBak)
                await self.consoleLog(f'Moving custom font "{i}" to CustomFont.bak', 'OPERATION')
                os.unlink(i)
                await asyncio.sleep(0.001)
            else:
                await self.consoleLog('Done moving custom font to CustomFont.bak', 'INFORMATION')

    async def backupOrigF(self):
        await self.retrieveVersion()
        if not os.path.isdir(self.OriginalFontBak): os.mkdir('OriginalRobloxFont.bak')
        for i in listdir(self.rootDict):
            if i.endswith('.txt') or i in listdir(self.OriginalFontBak):
                await self.consoleLog(f'Skipping {i}, already backed up or is a text file.', 'INFORMATION')
                continue
            await self.consoleLog(f'Creating backup of font: {i}', 'OPERATION')
            shutil.copy(f'{self.rootDict}/{i}', self.OriginalFontBak)
            await asyncio.sleep(0.001)

    async def createAddit(self):
        for i in listdir(self.rootDict):
            if i.endswith('.txt') or i in listdir(self.CustomFontBak):
                await self.consoleLog(f'{i} is text file or is already backed up', 'OPERATION')
                await asyncio.sleep(0.001)
                continue
            await self.consoleLog(f'Creating replacement font {i}', 'OPERATION')
            shutil.copy(f'{self.CustomFontBak}/arial.ttf', f'{self.CustomFontBak}/{i}')
            await asyncio.sleep(0.001)

    async def changeFont(self, mode=None):
        if mode == 'restore':
            for i in listdir(self.OriginalFontBak):
                if i in listdir(self.rootDict):
                    shutil.copy(f'{self.OriginalFontBak}/{i}', self.rootDict)
                    await self.consoleLog(f'Restoring file {i}', 'OPERATION')
                await asyncio.sleep(0.001)
            return
        if mode == 'all':
            await self.createAddit()
        for i in listdir(self.CustomFontBak):
            if i in listdir(self.rootDict):
                shutil.copy(f'{self.CustomFontBak}/{i}', f'{self.rootDict}')
                await self.consoleLog(f'Replacing font {i}', 'OPERATION')
                await asyncio.sleep(0.001)

    async def replaceFace(self):
        if not "face.png" is listdir(os.getcwd()):
            return
        shutil.copy(f'{os.getcwd()}/face.png', f'{self.rootDict[:-5]}textures')

    async def main(self):
        t0 = time.time()
        await asyncio.wait([self.retrieveVersion(), self.moveCustomFontToBak(),
                            self.backupOrigF()])
        await asyncio.wait([self.changeFont(self.mode),
                            self.replaceFace()])
        t1 = time.time()
        await self.consoleLog('Process took %.2f ms' % (1000*(t1-t0)), 'INFORMATION')
        input('Process took %.2f ms\nPress "Return" to close' % (1000*(t1-t0)))


#Input String
PrStr = """
Please type in the mode:
Standard | Standard mode, replaces only the found custom fonts.
All      | Replace all fonts, by duplicating the custom fonts to
           the supported fonts (custom font file must be named 'arial.ttf' without quotes).
           If you want multiple fonts, please put them with the correct file name in CustomFont.bak
Restore  | Restore Roblox's default font.
Exit     | Exit the program.

Alternatively you can place a 'face.png' in the same folder as the .exe or .py
> """

#call scripts
UIP = ''
while UIP.lower() not in ["standard", "all", "restore", "exit"]:
    os.system('cls' if os.name == 'nt' else 'clear')
    UIP = input(PrStr).lower()

if UIP != 'exit':
    os.system('cls' if os.name == 'nt' else 'clear')
    Flander(UIP)

os.unlink(pidfile)
sys.exit(0)
