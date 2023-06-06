"""Export lutris games to steam shortcuts""" ##
import binascii
import os
import re
import shlex
import shutil
import vdf
import glob
from pathlib import Path

STEAM_DATA_DIRS = (
    "~/.steam/debian-installation",
    "~/.steam",
    "~/.local/share/steam",
    "~/.local/share/Steam",
    "~/.steam/steam",
    "~/.var/app/com.valvesoftware.Steam/data/steam",
    "/usr/share/steam",
    "/usr/local/share/steam",
)
def search_recursive_in_steam_dirs(path_suffix):
    """Perform a recursive search based on glob and returns a
    list of hits"""
    results = []
    for candidate in STEAM_DATA_DIRS:
        glob_path = os.path.join(os.path.expanduser(candidate), path_suffix)
        for path in glob.glob(glob_path):
            results.append(path)
    return results


def get_config_path():
    config_paths = search_recursive_in_steam_dirs("userdata/**/config/")
    if not config_paths:
        return None
    return config_paths[0]


def get_shortcuts_vdf_path():
    config_path = get_config_path()
    if not config_path:
        return None
    return os.path.join(config_path, "shortcuts.vdf")


def vdf_file_exists():
    try:
        return bool(get_shortcuts_vdf_path())
    except Exception as ex:
        print("Failed to locate vdf file: %s", ex)
        return False

def matchid(shortcut):
    f = open("LastId", "r")
    if f.read() == str(shortcut.get('appid')):
        f.close()
        return True
    f.close()
    return False

def get_shortcuts():
    """Return all Steam shortcuts"""
    shortcut_path = get_shortcuts_vdf_path()
    if not shortcut_path or not os.path.exists(shortcut_path):
        return []
    with open(shortcut_path, "rb") as shortcut_file:
        shortcuts = vdf.binary_loads(shortcut_file.read())['shortcuts']
    return shortcuts


def shortcut_exists():
    try:
        shortcuts = get_shortcuts()
        if not shortcuts:
            return False
        return bool([s for s in shortcuts.values() if matchid(s)])
    except Exception as ex:
        print("Failed to read shortcut vdf file: %s", ex)
        return False
def create_shortcut():
    print("Creating Steam shortcut for PS Plus")
    shortcut_path = get_shortcuts_vdf_path()
    if os.path.exists(shortcut_path):
        with open(shortcut_path, "rb") as shortcut_file:
            shortcuts = vdf.binary_loads(shortcut_file.read())['shortcuts'].values()
    else:
        shortcuts = []

    shortcuts = list(shortcuts) + [generate_shortcut()]

    updated_shortcuts = {
        'shortcuts': {
            str(index): elem for index, elem in enumerate(shortcuts)
        }
    }
    with open(shortcut_path, "wb") as shortcut_file:
        shortcut_file.write(vdf.binary_dumps(updated_shortcuts))

def remove_shortcut(game):
    print("Removing Steam shortcut for %s", game)
    shortcut_path = get_shortcuts_vdf_path()
    if not shortcut_path or not os.path.exists(shortcut_path):
        return
    with open(shortcut_path, "rb") as shortcut_file:
        shortcuts = vdf.binary_loads(shortcut_file.read())['shortcuts'].values()
    other_shortcuts = [s for s in shortcuts if not matchid(s)]
    updated_shortcuts = {
        'shortcuts': {
            str(index): elem for index, elem in enumerate(other_shortcuts)
        }
    }
    with open(shortcut_path, "wb") as shortcut_file:
        shortcut_file.write(vdf.binary_dumps(updated_shortcuts))


def generate_preliminary_id():
    exe = f'"{Path.home()}/PS Now/psnowlauncher.exe"'
    unique_id = ''.join([exe])
    top = binascii.crc32(str.encode(unique_id, 'utf-8')) | 0x80000000
    return (top << 32) | 0x02000000


def generate_appid():
    return str(generate_preliminary_id() >> 32)


def generate_shortcut_id():
    preliminary_id = (generate_preliminary_id() >> 32) - 0x100000000
    with open('LastId', 'w') as f:
        f.write(str(preliminary_id))
    f.close()
    return preliminary_id


def generate_shortcut():
    shutil.which(str(Path.home()) + "/PS Now/psnowlauncher.exe")

    return {
        'appid': generate_shortcut_id(),
        'AppName': 'PS Plus',
        'Exe': f'"{str(Path.home())}/PS Now/psnowlauncher.exe"',
        'StartDir': f'"{str(Path.home())}/PS Now/"',
        'LaunchOptions': '',
        'IsHidden': 0,
        'AllowDesktopConfig': 1,
        'AllowOverlay': 1,
        'OpenVR': 0,
        'Devkit': 0,
        'DevkitOverrideAppID': 0,
        'LastPlayTime': 0,
    }

#print(get_shortcuts())
#create_shortcut()