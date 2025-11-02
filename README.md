# Star Citizen String Translation Merger Tool (Python Version)

> [!NOTE]
> Originally based on [ExoAE's ScCompLangPack](https://github.com/ExoAE/ScCompLangPack) idea and [MrKraken's SCLocalizationMergeTool](https://github.com/MrKraken/SCLocalizationMergeTool/) tools. I made this script to be able to customize components names, for other string of text it will still merge, but not customize.

> [!WARNING]
> Although I have created a tool to eliminate "most" manual process. If you are uneasy in running random python code from the internet, you can still manually adjust your localization file by just searching for the strings `CTRL`+`F` or simply running a find & replace with `CTRL`+`H`

> [!IMPORTANT]
> Due to my lack of ideas most of this readme will be copied from MrKraken's repo, i am sorry.

## Requirement
- Python >=3.8 (Tested on 3.11.9)

## 📝 What it Does
- Takes `target_strings.ini` as the input file & `global.ini` as source file from Data.p4k (use [StarFab](https://gitlab.com/scmodding/tools/starfab) to extract it)
- Finds the keys from input, matches them to source and replaces the value
- If the value is a ship component, it will customize it to add the component Type, Class and Grade, while also allowing for some color customization (very limited). See code comments in `makeTranslationFiles.py` for details
- Outputs `merged.ini`
- Optionally outputs directly to the specified game file. See code comments in `makeTranslationFiles.py` for details

## Customization
1. the provided `listof_components_with_grade_and_type.ini` contain the keys and name of all ship component, with their Class and Grade (from ExoAE's repo), this file must with the python script in the same folder as MrKraken's `merge-translations.ps1`
2. Open `makeTranslationFiles.py` in notepad (or other text editor)
3. Between line 18 and 51 is where you can edit code, follow each comment to see how to use the new functionalities
4. Line 51 has a customizable template for components name
    - The 5 booleans can be changed to False or True to disable certain customizations
    - The first two, `componentTypeShortened` and `componentClassShortened` will shorten the Type (COOL instead of Cooler) and the Class (Mili instead of Military) of the component
        - If you wish to, you can modify the two dictionary above each booleans
        - ONLY edit the string that is just after each comma ':' ("Cooler", "Shield", "Civi" or "Stlh")
    - The next 3, `componentTypeCapitalized`, `componentNameCapitalized` and `componentClassCapitalized` will allow you to capitalize or not the Type, Name and Class, which will override the capitalization of the lookup tables, but only that
5. You can verify the changes have taken effect by going to your install location → `data\Localization\english\global.ini` & searching for one of your strings using `CTRL`+`F`

## 🤔 Is this... legit?
> [!IMPORTANT]
> **Made by the Community** - This is an unofficial Star Citizen fan project, not affiliated with the Cloud Imperium group of companies. All content in this repository not authored by its host or users are property of their respective owners.
- The ability to customise your localisation using the extracted global.ini file is intended/authorised by CIG to support community made translations until it is officially integrated
    - *[Star Citizen: Community Localization Update](https://robertsspaceindustries.com/spectrum/community/SC/forum/1/thread/star-citizen-community-localization-update) 2023-10-11*
- Considered as third-party contributions, use at your own discretion
- [RSI Terms of Service](https://robertsspaceindustries.com/en/tos)
- [Translation & Fan Localization Statement](https://support.robertsspaceindustries.com/hc/en-us/articles/360006895793-Star-Citizen-Fankit-and-Fandom-FAQ#h_01JNKSPM7MRSB1WNBW6FGD2H98)

## Why did i do that ?
The short answer is that i was really bored and wanted to use the newly released tool to make a text format i liked when farming for components<br>
At first i was just modifying the strings manually with regex, but then i got curious and wanted to see if there was support for string formatting, as some games supports straight up HTML in text<br>
After more digging i found some interesting stuff in the global.ini, remnants of the common HTML tags, like \<i>, \<b> and even a \<span> with a style that set a background color, but sadly those seems to be extremely old and now deprecated.<br>
I did managed to find 4 tags that allow to change the color of the text that appear when you tractor beam an item, exactly what i wanted<br>
Sadly the 4 tags only allow to change to 4 preset color, blue (the same that you see in missions description to highlight poi), green, yellow and red, which isn't much but it's already that i guess.

This allow me to do THIS, which i think is really cool, even if very limited:<br>
<img width="316" height="88" alt="image" src="https://github.com/user-attachments/assets/e783fc78-ed9d-4fbb-991b-2906feb374fc" /><br>

Of course it would be too easy if everything worked the first try, so obviously something had to break.
The \<EM> tags do NOT work in the mobiglass (except in teh mission description for some reason), so when looking at a ship loadout this it what it'll look like:<br>
<img width="535" height="430" alt="image" src="https://github.com/user-attachments/assets/d4dc062d-d397-4c02-8e33-662520405360" /><br>

Yes it's almost unreadable, but you have the choice.

Keep the pretty color when tractor beaming stuff and have this ugly text when looking at ships loadout (the text is normal in inventories, it just doesn't have the color)<br>
Or, only keep the text but now it's all white and boring.

Until i find new way to customize text (if they exist) or until CIG update the game UI system to be something else than Adobe Flash, i don't think i'll be able to add anything.<br>
If by some miracle, you do know more tags/formatting/whatever, please share it, i want to try to make useful stuff for people to have a better time in the verse.

And if by a second miracle, a CIG employee is seeing this, please hire me. [e-mail](mailto:swann.sanchez9@outlook.fr)
