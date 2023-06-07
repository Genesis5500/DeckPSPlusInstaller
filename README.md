**PS Plus SteamDeck Installer**
==============

**What you have to do:**
1. Enter desktop mode
2. Open Konsole and run the following commands

```bash
git clone https://github.com/Genesis5500/DeckPSPlusInstaller.git
cd DeckPSPlusInstaller
chmod +x PSPlusInstaller
./PSPlusInstaller
```


**When the script finishes**
1. Restart Steam from Desktop mode and find the PS Plus non-Steam game from your library
2. Force Proton experimental for the application (video below these steps shows how to do that)
3. Start the PS Now shortcut from Steam
4. Right click on the Playstation icon from the system tray at the bottom of the screen
5. Select "Graphics Settings"
6. Uncheck "Optimize App performanace" and Apply
7. Return to Gaming mode
8. Give a try!

https://github.com/Genesis5500/DeckPSPlusInstaller/assets/135434827/7f16ec8b-b005-4f91-85a1-e65063e5126b

**What this script does:**
1. Checks for PSPlus files and needed DLL
2. Downloads and extracts to HOME
3. Sets Steam shortcut for application

**Things to Note**
1. You may have to sign in twice, not sure the reasoning for this
2. Once started, controller support should look like a TV & Controller icon in the top right hand corner of the sceen
3. Keep clicking this using the touchpad until it responds, full-screen may work as well this way
4. If the shortcut does not create itself in Steam, you can it manually by doing the following

   1. Go to Steam -> Add non-steam game -> Browse -> Home/PS Now/psnowlaunher.exe
   2. Add it and set to run with Proton Experimental

**Huge Shoutout to https://www.youtube.com/@SteamDeckGaming & the creators of Lutris for making this possible!**
