import os.path, sys
from pathlib import Path
import tarfile
import wget
import asyncio
import gdown
import shortcut
import ssl


PROTONURL = 'https://github.com/GloriousEggroll/proton-ge-custom/releases/download/6.21-GE-2/Proton-6.21-GE-2.tar.gz'
PSNOWURL = 'https://drive.google.com/drive/folders/1If6H3SYoYK66HEcVnMlXk_LtP7rpcFve'
PROTONZIP = 'Proton-6.21-GE-2.tar.gz'
PROTONDIR = 'Proton-6.21-GE-2'
PSPLUSTAR = 'psplusfiles.tar.gz'
STEAMCOMPATTOOLSPATH = str(Path.home()) + '/.steam/root/compatibilitytools.d'

#create this bar_progress method which is invoked automatically from wget
def bar_progress(current, total, width=80):
  progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
  # Don't use print() as it will print in new line every time.
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()


def checkforprotonzip():
    # First check and see if Proton is installed in compat tools first thing
    if (os.path.isdir(STEAMCOMPATTOOLSPATH + '/' + PROTONDIR)):
        print('Proton already installed correctly!')
        return True
    if not os.path.isfile(PROTONZIP):
        print("Correct Proton version not found. Downloading now... ")
        return False
    else:
        print("Found Proton zip! Checking if Steam compat folder exists... ")
        return  True

async def DownloadProton():
    # Download the Proton tar
    try:
        wget.download(PROTONURL, bar=bar_progress)
    except Exception as e:
        print(e)

async def checkforsteamcompattooldir():
    print('Checking for compat tools path in Steam... ')
    if not os.path.isdir(STEAMCOMPATTOOLSPATH):
        print('Not found! Creating folder... ')
        os.makedirs(STEAMCOMPATTOOLSPATH, exist_ok=False)
        if os.path.isdir(STEAMCOMPATTOOLSPATH):
            print('Done! Extracting Proton version to directory... ')
            await ExtractProton()
        else:
            print('Could not create Steam compat tools directory!')
    else:
        print('Found compat tools folder! Extracting Proton version to directory... ')
        await ExtractProton()

async def ExtractProton():
    if not (os.path.isdir(STEAMCOMPATTOOLSPATH + '/' + PROTONDIR)):
        file = tarfile.open(PROTONZIP)
        # extracting file to compat tools
        file.extractall(STEAMCOMPATTOOLSPATH)
        # Close the file
        file.close()
        print('Extraction complete!')
    else:
        print('Proton already extracted properly!')

def checkprotoninstall():
    if (os.path.isdir(STEAMCOMPATTOOLSPATH + '/' + PROTONDIR)):
        return True
    return False

def checkpsplusextracted():
    if os.path.isdir(str(Path.home()) + '/PS Now/'):
        return True
    return False

def getpsplusfiles():
    print('Checking for PSPlus zip file... ')
    if checkpsplusextracted() is True:
        print('PS Plus already extracted!')
    elif not os.path.isfile(PSPLUSTAR):
        print('Not found! Downloading now... ')
        output = PSPLUSTAR
        try:
            url = "https://drive.google.com/file/d/1hB_ltEpXYTS2hYFXb9qwQsuia063AyRT/view?usp=sharing"
            gdown.download(url=url, output=output, fuzzy=True)
            getpsplusfiles()
        except Exception as e:
            print(e)
    else:
        print('Found!')
        checkifpsplusextracted()

async def checkifpsplusextracted():
    if os.path.isdir(str(Path.home()) + '/PS Now/'):
        print('PS Now already extracted properly!')
    else:
        print('Zip not extracted! Extracting now... ')
        await extractpsplusfiles()

async def extractpsplusfiles():
    file = tarfile.open(PSPLUSTAR)
    # extracting file to compat tools
    file.extractall(Path.home())
    # Close the file
    file.close()
    print('Extraction complete!')

async def main():
    ssl._create_default_https_context = ssl._create_unverified_context

    if checkforprotonzip() is False and checkprotoninstall() is False:
        try:
            await DownloadProton()
        except Exception as e:
            print(e)


    await checkforsteamcompattooldir()

    try:
        if (checkprotoninstall() is True):
            getpsplusfiles()
            if (shortcut.shortcut_exists() is True):
                print('Shortcut already added to Steam.')
            else:
                print('Adding shortcut to Steam... ')
                shortcut.create_shortcut()
                print('Done!')
    except Exception as e:
        print(e)

asyncio.run(main())
