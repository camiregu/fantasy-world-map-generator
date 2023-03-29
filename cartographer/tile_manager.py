#camiregu
#2023-mar-28
import config
import pygame as pg


#tile class
class Tile(pg.sprite.Sprite):
    def __init__(self, coordinates: tuple[int,int,int]) -> None:
        super().__init__(unfilled)
        self.image = UNEXPLORED_IMAGE
        self.coordinates = coordinates
        tiles.update({self.coordinates: self})
        return
        
    def update_terrain(self, terrain: str):
        self.terrain = terrain
        self.image = TERRAIN_IMAGES[terrain]
        return

    def set_explored(self, explored: bool):
        if explored:
            unfilled.remove(self)
            filled.add(self)
        else:
            unfilled.add(self)
            filled.remove(self)
        return

    def mouse_is_over(self) -> bool:
        mouse_pos = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
    


#functions
def start_tiles():
    #constants
    global TERRAIN_IMAGES, UNEXPLORED_IMAGE

    #global variables
    global unfilled, filled, tiles

    TERRAIN_IMAGES = {}
    for terrain_name, image_path in config.TERRAINS.items():
        TERRAIN_IMAGES.update({terrain_name: pg.image.load(image_path)})
    UNEXPLORED_IMAGE = pg.image.load(config.UNEXPLORED_IMAGE_PATH)

    unfilled = pg.sprite.Group()    
    filled = pg.sprite.Group()
    tiles = {}
    return


def download_map(tilemap: dict):
    for coordinates, terrain in tilemap.items():
        tile = Tile(coordinates)
        tile.update_terrain(terrain)
        tile.set_explored(True)
    return


def upload_map() -> dict:
    tilemap = {}
    for tile in tiles.values():
        if unfilled not in tile.groups():
            tilemap.update({tile.coordinates: tile.terrain})
    return tilemap