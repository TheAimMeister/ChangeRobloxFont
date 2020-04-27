# ChangeRobloxFont
A little script that I wrote in python 3.7.4 that runs a code that replaces the font automatically.
I mainly made it for Phantom Forces, but you can use every font used within the roblox directory.
Alternatively, you can also change it for Phantom Forces first, as the program will create a backup of Roblox's original font

a Python package called "PyInstaller" has been used to create the .exe file

# Requirements
Windows
   - can run the .exe without python installed; Or one can install python to run the python file instead.
   - the .exe file may generate a windows safescreen warning as there's no digital signature

note: I don't own a MacOs or Linux, so I have no clue if they're compatible.

# Current Errors
Error code 480 (description unknown at this point, halting a fix.)

# Download the correct version at:
https://github.com/TheAimMeister/ChangeRobloxFont/releases

# How to use:
1. Download a font

2. Place the font(s) and the .exe in a directory

3. Check if the fonts names are, and if not rename them to(.otf extension will also work):
   - Regular.ttf
   - Bold.ttf
   - Light.ttf

3.1 If the font consists of only one .ttf or .otf file,
        create copies and rename them to the names listed at step 3

4. Run the .exe


# CHANGELOG
Changes from v0.0.5:
- Reduced the amount of I/O calls
- Slight improvement in performance
- Removed "All" operation, this is now become the standard operation
- No longer need arial.ttf, instead you need to use Regular.ttf, Bold.ttf, Light.ttf

Hotfix from v0.0.5a:
 - Fixed a typo that caused the face.png not to change (didn't threw an error when testing; Henche why the hotfix is late.)

v0.0.5a:
 - Rewritten code again
 - Output now goes to console.txt
 - Added async to speed up things a bit as well for stability

v0.0.4a:
 - Rewritten the code, should gain a bit performance and should be easier to read
 - A better way of handling the .pid file, if for some reason you might crash the program you can delete the created 'ChangeFont.pid' safely

v0.0.3a:
   - Added a little menu before it starts operating
   - Update: forgot to add an exit option, so here it is
   
v0.0.2b:
   - Cleans up fonts from the main folder and copy/moves them to CustomFont.bak

v0.0.2a:
   - Fixed up backup script
   - Attempt on fixing error 480
