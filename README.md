# Roblox Font Changer
A little script that I wrote in python 3.8.3 that runs a code which replaces Roblox font automatically each time you open the file.
I mainly made it for Phantom Forces, but you can use every font used within the roblox directory.
Alternatively, you can also change it for Phantom Forces first, as the program will create a backup of Roblox's original font

a Python package called "PyInstaller" has been used to create the .exe file

# Requirements
Windows only
   - can run the .exe without python installed; Or one can install python to run the python file instead.
   - the .exe file may generate a windows safescreen warning as there's no digital signature

# Current Errors
None

# Download the correct version at:
https://github.com/TheAimMeister/ChangeRobloxFont/releases

# How to use:
1. Download a font

2. Place the font(s) and the .exe or .py in a directory

3. Check if the fonts names are, and if not rename them to(.otf extension will also work):
   - regular.ttf

4. Run the .exe or the .py file


# CHANGELOG
Changes from v0.0.7a:
- Local fonts are now saved in memory
- Script will now ask which font to use if multiple are found
- Now requires regular.ttf instead of arial.ttf, which will be used if a font is not found

I forgot to mention some stuff and update this.., oopsie.

Changes from v0.0.6:
- Removed the class operator
- No longer uses asynchronous functions
- Makes use of logging
- Back to requiring arial.ttf (sorry)
- Moved the time.sleep to it's own function and it's called after each shutil.copy()
- Script now waits for shutil.copy() to be completed
- Removed the requirement for user input
- Restoring the default font function now has it's own file

Changes from v0.0.5:
- Reduced the amount of I/O calls
- Slight improvement in performance
- Removed "All" operation, this is now become the standard operation
- No longer need arial.ttf, instead you need to use Regular.ttf, Bold.ttf, Light.ttf
