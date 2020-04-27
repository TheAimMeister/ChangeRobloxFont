import os, shutil, sys, time, asyncio, datetime, zipfile
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
    CustomFont = [f for f in listdir(os.getcwd()) if f.endswith('.otf' or '.ttf') and f[:-4] in ["Regular", "Light", "Bold"]]
    allCompatFiles = None
    replacedFonts = []
    consoleMem = []

    def __init__(self, mode):
        self.mode = mode
        if not os.path.isdir(self.OriginalFontBak): os.mkdir("OriginalRobloxFont.bak")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())
        loop.close()

    async def consoleLog(self, context, type, finalize=False):
        if not finalize:
            self.consoleMem.append((f'[{datetime.datetime.now()}] {type} | {context}\n'))
        else:
            with open("console.txt", 'a+') as f:
                for i in self.consoleMem:
                    f.write(i)

    async def retrieveVersion(self):
        for (dirpath, dirnames, filenames) in walk(self.rootDict):
            if "RobloxPlayerBeta.exe" in filenames:
                await self.consoleLog(f'Found version at: {dirpath}', 'OPERATION')
                self.rootDict = f'{dirpath}/content/fonts'
                break

    async def backupFonts(self):
        try:
            await asyncio.wait_for(self.retrieveVersion(), timeout=5.0)
        except asyncio.TimeoutError:
            print("We ran into a timeout problem, failed to retrieve version.")
            sys.exit(0)
        self.allCompatFiles = [f for f in listdir(self.rootDict) if not f.endswith('.txt')]
        for i in self.allCompatFiles:
            if not i in listdir(self.OriginalFontBak):
                await self.consoleLog(f'Creating backup of font: {i}', 'OPERATION')
                shutil.copy(f'{self.rootDict}/{i}', self.OriginalFontBak)
                await asyncio.sleep(0.001)

    async def moveCustomFontToBak(self):
        try:
            await asyncio.wait_for(self.backupFonts(), timeout=5.0)
        except asyncio.TimeoutError:
            print("We ran into a timeout problem, failed to complete font backup.")
            sys.exit(0)
        if not os.path.isdir(self.CustomFontBak): os.mkdir('CustomFont.bak')
        for f in self.allCompatFiles:
            for i in self.CustomFont:
                if i[:-4] in f:
                    await self.consoleLog(f'Creating replacement for {f}', 'OPERATION')
                    shutil.copy(f'{os.getcwd()}/{i}', f'{self.CustomFontBak}/{f}')
                    self.replacedFonts.append(f)
                    break
            if not f in self.replacedFonts:
                await self.consoleLog(f'Creating replacement for {f}', 'OPERATION')
                shutil.copy(f'{os.getcwd()}/Regular.otf' or f'{os.getcwd()}/Regular.ttf', f'{self.CustomFontBak}/{f}')

    async def changeFont(self, mode=None):
        if mode == 'restore':
            for i in listdir(self.OriginalFontBak):
                if i in listdir(self.rootDict):
                    shutil.copy(f'{self.OriginalFontBak}/{i}', self.rootDict)
                    await self.consoleLog(f'Restoring file {i}', 'OPERATION')
                await asyncio.sleep(0.001)
            return
        if mode == 'standard':
            for i in listdir(self.CustomFontBak):
                if i in listdir(self.rootDict):
                    shutil.copy(f'{self.CustomFontBak}/{i}', f'{self.rootDict}')
                    await self.consoleLog(f'Replacing font {i}', 'OPERATION')
                    await asyncio.sleep(0.001)

    async def replaceFace(self):
        if not "face.png" in listdir(os.getcwd()):
            return
        shutil.copy(f'{os.getcwd()}/face.png', f'{self.rootDict[:-5]}textures')

    async def main(self):
        t0 = time.time()
        if self.mode != "restore":
            await asyncio.wait([self.retrieveVersion(), self.backupFonts(),
                                self.moveCustomFontToBak()])
            await asyncio.wait([self.changeFont(self.mode),
                                self.replaceFace()])
        else:
            await self.changeFont(self.mode)
        t1 = time.time()
        await self.consoleLog('Process took %.2f ms' % (1000*(t1-t0)), 'INFORMATION')
        await self.consoleLog("Finalize", "OPERATION", True)
        input('Process took %.2f ms\nPress "Return" to close' % (1000*(t1-t0)))


#Input String
PrStr = """
Please type in the mode:
Standard | Replaces all fonts
Restore  | Restore Roblox's default font.
Exit     | Exit the program.

Alternatively you can place a 'face.png' in the same folder as the .exe or .py
> """

#call scripts
UIP = ''
while UIP.lower() not in ["standard", "restore", "exit"]:
    os.system('cls' if os.name == 'nt' else 'clear')
    UIP = input(PrStr).lower()

if UIP != 'exit':
    os.system('cls' if os.name == 'nt' else 'clear')
    Flander(UIP)

os.unlink(pidfile)
sys.exit(0)
