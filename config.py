#camiregu
#2023-mar-24
import json
import os

with open("global_config.json","r") as global_config:
    GLOBAL_SETTINGS: dict = json.load(global_config)
    STORAGE_FILENAME: str = GLOBAL_SETTINGS["storage_filename"]
    LOCAL_CONFIG_FILENAME: str = GLOBAL_SETTINGS["local_config_filename"]
    TILEMAP_FILENAME: str = GLOBAL_SETTINGS["tilemap_filename"]
    TEXTURE_DIRECTORY: str = GLOBAL_SETTINGS["texture_directory"]
    BASIS_VECTORS: list[list[int]] = GLOBAL_SETTINGS["basis_vectors"]

def load_local_settings(local_path: str):
    global TERRAINS
    global INCIRCLE_RADIUS
    global UNEXPLORED_IMAGE_PATH

    INCIRCLE_RADIUS = 100
    TERRAINS = {
        "arctic": "textures\\arctic.png",
        "desert": "textures\\desert.png",
        "forest": "textures\\forest.png",
        "hills": "textures\\hills.png",
        "lake": "textures\\lake.png",
        "mountains": "textures\\mountains.png",
        "ocean": "textures\\ocean.png",
        "plains": "textures\\plains.png",
        "swamp": "textures\\swamp.png",
    }
    UNEXPLORED_IMAGE_PATH = "textures\\unexplored.png"
    #with open(local_path, "r") as local_config:
    #    LOCAL_SETTINGS: dict = json.load(local_config)
    #    TERRAINS: dict = LOCAL_SETTINGS["terrains"]
    #    INCIRCLE_RADIUS: int = LOCAL_SETTINGS["incircle_radius"]
