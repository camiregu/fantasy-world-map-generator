# camiregu
# 2023-mar-22
from config import Config
import os
import json
import shutil

# functions
def get_map_names() -> list[str]:
    """Return a list of all map names.""" #TODO remove the need for maps.json
    return os.listdir(Config.MAPS_DIRECTORY)


def create_map_files():
    """Create map folder and storage files in the maps directory."""
    #create folder, tilemap and local config files
    #update maps.json
    pass


def delete_map(map_name: str) -> None:
    """Delete map directory and children."""
    map_path = os.path.join(Config.MAPS_DIRECTORY, map_name)
    shutil.rmtree(map_path)


def edit_map(map_name: str, new_settings: dict) -> None:
    """Edit map directory name and config file."""
    config_path = os.path.join(Config.MAPS_DIRECTORY, map_name, Config.LOCAL_CONFIG_FILENAME)
    
    with open(config_path, "r") as local_config:
        config: dict = json.load(local_config)

    config.update(new_settings)

    with open(config_path,"w") as local_config:
        json.dump(config, local_config)


def duplicate_map(map_name: str) -> None:
    """Create a new copy of selected map, with a different name."""
    config_path = os.path.join(Config.MAPS_DIRECTORY, map_name, Config.LOCAL_CONFIG_FILENAME)

    i, new_map_name = 1, map_name + ' (1)'
    while new_map_name in get_map_names():
        i += 1
        new_map_name = map_name + f' ({i})'

    new_map_path = os.path.join(Config.MAPS_DIRECTORY, new_map_name)
    os.makedirs(new_map_path)
    shutil.copy(config_path, new_map_path)



def remove_illegal_chars(string: str) -> str:
    return string.replace("<","").replace(">","").replace(":","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","").strip(" .")