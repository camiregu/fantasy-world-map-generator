#camiregu
#2023-mar-24
import config
import numpy as np
import pygame as pg
import random

#tile class
class Tile(pg.sprite.Sprite):
    def __init__(self, coordinates: tuple[int,int,int]) -> None:
        super().__init__(unfilled_tiles)
        self.image = UNEXPLORED_IMAGE
        self.coordinates = coordinates
        self.rect = pg.Rect(get_screen_pos(self.coordinates) + BLIT_OFFSET, RECT_SIZE)
        tiles.update({self.coordinates: self})
        
    def update_terrain(self, terrain: str):
        self.terrain = terrain
        self.image = TERRAIN_IMAGES[terrain]

    def set_explored(self, explored: bool):
        if explored:
            unfilled_tiles.remove(self)
            filled_tiles.add(self)
        else:
            unfilled_tiles.add(self)
            filled_tiles.remove(self)

    def mouse_is_over(self):
        mouse_pos = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
    
#functions
def download_map(tilemap: dict):
    restart_map()
    for coordinates, terrain in tilemap.items():
        tile = Tile(coordinates)
        tile.update_terrain(terrain)
        tile.set_explored(True)
    set_tiles = tuple(tiles.values())
    for tile in set_tiles:
        surround_tile(tile)
    filled_tiles.draw(DISPLAY)
    unfilled_tiles.draw(DISPLAY)
    pg.display.flip()


def upload_map() -> dict:
    tilemap = {}
    for tile in tiles.values():
        if unfilled_tiles not in tile.groups():
            tilemap.update({tile.coordinates: tile.terrain})
    return tilemap


def restart_map():
    #constants
    global BLIT_OFFSET
    global RECT_SIZE
    global AXIS_VECTORS
    global DISPLAY
    global ORIGIN
    global TERRAIN_IMAGES
    global UNEXPLORED_IMAGE

    #global variables
    global scaling_factor
    global unfilled_tiles
    global filled_tiles
    global tiles

    BLIT_OFFSET = ((-2 / np.sqrt(3)) * config.INCIRCLE_RADIUS)
    RECT_SIZE = -2*BLIT_OFFSET, -2*BLIT_OFFSET
    AXIS_VECTORS = (
        np.array((-1/2, -np.sqrt(3)/2)) * (2/np.sqrt(3)) * config.INCIRCLE_RADIUS,
        np.array((-1/2, np.sqrt(3)/2)) * (2/np.sqrt(3)) * config.INCIRCLE_RADIUS,
        np.array((1,0)) * (2/np.sqrt(3)) * config.INCIRCLE_RADIUS
    )
    DISPLAY = pg.display.set_mode((0,0),pg.WINDOWMAXIMIZED)
    ORIGIN = np.array((DISPLAY.get_width() // 2, DISPLAY.get_height() // 2))
    TERRAIN_IMAGES = {}
    for terrain_name, image_path in config.TERRAINS.items():
        TERRAIN_IMAGES.update({terrain_name: pg.image.load(image_path)})
    UNEXPLORED_IMAGE = pg.image.load(config.UNEXPLORED_IMAGE_PATH)

    scaling_factor = 1
    unfilled_tiles = pg.sprite.Group()    
    filled_tiles = pg.sprite.Group()
    tiles = {}


def surround_tile(tile: Tile):
    for vector in config.BASIS_VECTORS:
        pos_1 = tuple(tile.coordinates + np.array(vector))
        if (pos_1 not in list(tiles.keys())):
            Tile(pos_1)
        pos_2 = tuple(tile.coordinates - np.array(vector))
        if (pos_2 not in list(tiles.keys())):
            Tile(pos_2)


def fill_tile(tile: Tile):
    terrain = assign_terrain(tile.coordinates)
    tile.update_terrain(terrain)
    tile.set_explored(True) 
    surround_tile(tile)


def assign_terrain(coordinates: tuple) -> str:
    probability_list = []
    for vector in config.BASIS_VECTORS:
        pos_1 = tuple(coordinates + np.array(vector))
        if (pos_1 in list(tiles.keys()) and unfilled_tiles not in tiles[pos_1].groups()):
            probability_list += [tiles[pos_1].terrain] * 3
        else:
            i = random.randrange(len(TERRAIN_IMAGES))
            possible_terrain = list(TERRAIN_IMAGES.keys())[i]
            probability_list += [possible_terrain] * 2

        pos_2 = tuple(coordinates - np.array(vector))
        if (pos_2 in list(tiles.keys()) and unfilled_tiles not in tiles[pos_2].groups()):
            probability_list += [tiles[pos_2].terrain] * 3
        else:
            i = random.randrange(len(TERRAIN_IMAGES))
            possible_terrain = list(TERRAIN_IMAGES.keys())[i]
            probability_list += [possible_terrain] 
    return probability_list[random.randrange(len(probability_list))]


def process_user_input() -> bool:
    events = pg.event.get()
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 2:
            pg.quit()
            return True
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for tile in unfilled_tiles:
                if tile.mouse_is_over():
                    fill_tile(tile)
    
    unfilled_tiles.draw(DISPLAY)
    filled_tiles.draw(DISPLAY)
    pg.display.flip()
    return False


def get_screen_pos(coordinates: tuple[int,int,int]) -> np.ndarray:
    return coordinates[0] * AXIS_VECTORS[0] + coordinates[1] * AXIS_VECTORS[1] + coordinates[2] * AXIS_VECTORS[2] + ORIGIN

#constants


restart_map()