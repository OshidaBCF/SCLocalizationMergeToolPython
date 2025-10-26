import os, re, sys, shutil
key, componentType, componentClass, componentGrade, componentName = None, None, None, None, None

##################
# String processing file - Originally from /u/Asphalt_Expert's component stats language pack_ https://github.com/ExoAE/ScCompLangPack/blob/main/merge-process/merge-ini.ps1
# Given a bit of piss and vinegar by MrKraken (https://www.youtube.com/@MrKraken)
# Converted in Python script by Oshida
# Create translations file for different configuration possible
# Output result in the "output" folder as a global.ini
# If line below is set to true, the global.ini will also be pasted in the defined global.ini game path
# After any update, global.ini in the scr folder should be updated with the new version, extract it using starFab https://gitlab.com/scmodding/tools/starfab
##################

################## !!!! ##############
# YOU SHOULD ONLY EDIT BELOW THIS LINE
################## !!!! ##############

# User config - you can change these values
gameInstallPath = R'C:\Program Files\Roberts Space Industries\StarCitizen\Game' # Set your game installation path here
gameIniWrite = True # Set to True if you want to write directly the global.ini to the game folder

# Those are the Shortened version of the Component type, only change the word after the ':', do NOT modify the 4 leter word
componentTypeLookup = {"COOL" : "Cooler", "POWR" : "Power Plant", "SHLD" : "Shield", "QDRV" : "Quantum Drive"}
componentTypeShortened = False

# Those are the Shortened version of the Component type, only change the 4 leter after the ':', do NOT modify the longer word
componentClassLookup = {"Military" : "Mili", "Civilian" : "Civi", "Competition" : "Comp", "Stealth" : "Stlh", "Industrial" : "Indu"}
componentClassShortened = False


# This is to change if you want the Type, Name and/or Class to be Capitalized
componentTypeCapitalized = True
componentNameCapitalized = False
componentClassCapitalized = True

# You can modify this string so that all component will follow a specific template
# The string can contain all, some or none of the variable
# The 4 available variables are
# {componentType} : The type of the component (Cooler, Shield)
# {componentClass} : The class of the component (Stealth, Military)
# {componentGrade} : The grade of the component (A, C)
# {componentName} : The name of the component
# The {} are REQUIRED, you can put text around like this [{componentType}] and it'll show as [Cooler]
# You can also put <EM1-4></EM1-4> around text to give it a color (<EM2>[{componentClass} {componentGrade}]</EM2>)
# EM1 will color the text in blue, the same blue that highlight important texts in mission
# EM2 will color the text in green
# EM3 will color the text in yellow
# EM4 will color the text in red
# Without an EM tag, the text will be the default white/cyan

formatedString = '[{componentType}] <EM2>[{componentClass} {componentGrade}]</EM2> <EM1>{componentName}</EM1>' # Exemple on readme.md

################## !!!! ##############
# YOU SHOULD ONLY EDIT ABOVE THIS LINE
################## !!!! ##############

scriptDir =  os.getcwd()# Get the script directory
targetStringsPath = scriptDir + '/target_strings.ini' # input file
globalIniPath = scriptDir + '/src\global.ini' # source file from Data.p4k
mergedIniPath = scriptDir + '/output\merged.ini' # Output file

# Check if files exist first, make folders for outpuits if we need them
if (not os.path.exists(targetStringsPath)):
    print("target_strings.ini not found at: {targetStringsPath}")
    sys.exit()

if (not os.path.exists(globalIniPath)):
    print("global.ini not found at: {$globalIniPath}")
    sys.exit()

if (not os.path.exists(gameInstallPath)):
    print("Directory not found: {$gameInstallPath}")
    sys.exit()

outputDir = scriptDir + '/output'
if (not os.path.exists(outputDir)):
    os.mkdir(outputDir)
    print("Created output directory: {outputDir}")

gameIniPath = gameInstallPath + '/data\Localization\english\global.ini' # now we know the install folder is valid we can stitch on the localization path
if (gameIniWrite):
    gameLocalizationDir = gameInstallPath + '/data\Localization\english'
    if (not os.path.exists(gameLocalizationDir)):
        os.mkdir(gameLocalizationDir)
        print("Created game localization directory: {gameLocalizationDir}")


# Load target_strings.ini into a hashtable (key -> new value)
replacements = {}
with open(targetStringsPath, 'r', encoding="utf-8-sig") as targetStringsFile:
    for line in targetStringsFile.readlines():
        search = re.match('^(.*)=(.*)$', line)
        if (search):
            key = search.group(1)
            value = search.group(2)
            replacements[key] = value

# Processing replacement for customization
for key, value in replacements.items():
    search = re.match("^item_[nN]ame_?([A-Z]{4})[a-zA-Z0-9_]*$", key) 
    componentType = search.group(1)
    
    search = re.match("^(['a-zA-Z0-9\- ]*) ([a-zA-Z0-9\-]*) ([A-Z])$", value)    
    componentName = search.group(1)
    componentClass = search.group(2)
    componentGrade = search.group(3)
    
    if not componentTypeShortened:
        componentType = componentTypeLookup[componentType]
    
    if componentClassShortened:
        componentClass = componentClassLookup[componentClass]
    
    if componentTypeCapitalized:
        componentType = componentType.upper()
    
    if componentClassCapitalized:
        componentClass = componentClass.upper()
    
    if componentNameCapitalized:
        componentName = componentName.upper()
    replacements[key] = formatedString.format(componentType = componentType, componentClass = componentClass, componentGrade = componentGrade, componentName = componentName)
    #print(replacements[key])

# global.ini pre process because there's some weird bytes that like to break stuff
with open(globalIniPath, 'rb+') as globalIniFile:
    data = globalIniFile.read()
    data = data.replace(b'\xc2\xa0', b'\x20')
    data = data.replace(b'\xa0', b'\x20')
    globalIniFile.seek(0)
    globalIniFile.write(data)
    globalIniFile.truncate()
    globalIniFile.close()
        
# Process global.ini line by line and only replace values for keys found in the hashtable
globalHashTable = {}
with open(globalIniPath, encoding="utf-8-sig") as globalIniFile:
    for line in globalIniFile.readlines():
        search = re.match('^([^=]*)=(.*)$', line)
        if (search):
            key = search.group(1)
            if (key in replacements):
                value = replacements[key]
            else:
                value = search.group(2)
            globalHashTable[key] = value

# Write to merged.ini
with open(mergedIniPath, 'w', encoding="utf-8-sig") as mergedIniFile:
    for key, value in globalHashTable.items():
        mergedIniFile.write(f"{key}={value}\n")
    mergedIniFile.close()

# Copy to game path if gameIniWrite is True
if (gameIniWrite):
    shutil.copyfile(mergedIniPath, gameIniPath)