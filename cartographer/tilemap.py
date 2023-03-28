#camiregu
#2023-mar-27
import json

#functions
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