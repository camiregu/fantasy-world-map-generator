# camiregu
# 2023-mar-27
from config import Config
from cartographer.tile_manager import TileManager
from cartographer.display_controller import DisplayController
import cartographer.event_processor as ep

import os
import json


# functions
def open_map(local_directory: str):
    tilemap_path = os.path.join(Config.MAPS_DIRECTORY, local_directory, Config.TILEMAP_FILENAME)
    local_config_path = os.path.join(Config.MAPS_DIRECTORY, local_directory, Config.LOCAL_CONFIG_FILENAME)

    Config.load_local_settings(local_config_path)
    tilemap = download_map(tilemap_path)

    DisplayController.start()
    TileManager.start(DisplayController.draw_surface)
    TileManager.load(tilemap)
    
    done = False
    DisplayController.draw_screen()
    while not done:
        done = ep.process_user_input()
    tilemap = TileManager.save()
    upload_map(tilemap,tilemap_path)


def download_map(file_path: str) -> dict:
    with open(file_path,"r") as tilemap_file:
        tilemap = json.load(tilemap_file)
    tiles = {}
    for key, value in tilemap.items():
        tiles.update({tuple(json.loads("[" + key + "]")): value})
    return tiles


def upload_map(tiles: dict, file_path):
    tilemap = {}
    for key, value in tiles.items():
        tilemap.update({str(key)[1:-1]: value})
    with open(file_path,"w") as tilemap_file:
        json.dump(tilemap, tilemap_file)