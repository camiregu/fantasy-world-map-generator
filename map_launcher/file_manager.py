# camiregu
# 2023-mar-22
from config import Config
import json
import os
import shutil

# functions
def get_map_names() -> list[str]:
    """Return a list of all map names.""" #TODO remove the need for maps.json
    with open(Config.STORAGE_FILENAME, "r") as storage:
        map_list = json.load(storage)['maps']
    return map_list


def create_map_files():
    """Create map folder and storage files in the maps directory."""
    #create folder, tilemap and local config files
    #update maps.json
    pass


def delete_map(map: str) -> None:
    """Delete map folder and children, and remove it from the map list."""
    #delete folder and children
    #remove world from maps.json
    pass


def edit_map(map: str, settings: dict) -> None:
    """Edit map directory name and config file."""
    #change folder name
    #update local config
    pass

def remove_illegal_chars(string: str) -> str:
    return string.replace("<","").replace(">","").replace(":","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","").strip(" .")