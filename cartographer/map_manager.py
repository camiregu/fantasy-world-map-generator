#camiregu
#2023-mar-27
import config
import cartographer.tile_manager as tm
import cartographer.event_processor as ep
import cartographer.map_painter as mp

import os
import json


#functions
def open_map(local_directory: str):
    tilemap_path = os.path.join(local_directory,config.TILEMAP_FILENAME)
    local_config_path = os.path.join(local_directory,config.LOCAL_CONFIG_FILENAME)

    config.load_local_settings(local_config_path)
    map = load_map(tilemap_path)

    tm.start_tiles()
    tm.download_map(map)
    mp.start_map()

    done = False
    while not done:
        done = ep.process_user_input()
    map = tm.upload_map()
    save_map(map,tilemap_path)


def load_map(file_path: str):
    with open(file_path,"r") as tilemap_file:
        tilemap = json.load(tilemap_file)
    tiles = {}
    for key, value in tilemap.items():
        tiles.update({tuple(json.loads("[" + key + "]")): value})
    return tiles


def save_map(tiles: dict, file_path) -> None:
    tilemap = {}
    for key, value in tiles.items():
        tilemap.update({str(key)[1:-1]: value})
    with open(file_path,"w") as tilemap_file:
        json.dump(tilemap, tilemap_file)