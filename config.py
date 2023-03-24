#camiregu
#2023-mar-24
import json

with open("global_config.json","r") as global_config:
    SETTINGS: dict = json.load(global_config)
    STORAGE_FILENAME = SETTINGS["storage_filename"]
    LOCAL_CONFIG_FILENAME = SETTINGS["local_config_filename"]
    TILEMAP_FILENAME = SETTINGS["tilemap_filename"]
    TEXTURE_DIRECTORY = SETTINGS["texture_directory"]