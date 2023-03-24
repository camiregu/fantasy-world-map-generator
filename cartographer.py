#camiregu
#2023-mar-24
import config
import time
import json
import numpy as np
import pygame as pg
import os

#constants
SCALING_FACTOR = 1
INNER_TILE_RADIUS = 100
AXIS_VECTORS = [
    np.array((-1/2, -np.sqrt(3)/2)) * (2/np.sqrt(3)) * INNER_TILE_RADIUS,
    np.array((-1/2, np.sqrt(3)/2)) * (2/np.sqrt(3)) * INNER_TILE_RADIUS,
    np.array((1,0)) * (2/np.sqrt(3)) * INNER_TILE_RADIUS
]

WHITE_TILE_NAME = "white.png"
GREEN_TILE_NAME = "green.png"
DARK_TILE_NAME = "dark.png"
BLIT_OFFSET = ((-2 / np.sqrt(3)) * INNER_TILE_RADIUS)

#tile class
class Tile(pg.sprite.Sprite):
    def __init__(self, coordinates: tuple[int,int,int]) -> None:
        super().__init__(unfilled_tiles)
        self.update_terrain("unexplored")
        self.rect = pg.Rect(get_screen_pos(coordinates) + BLIT_OFFSET, (-2*BLIT_OFFSET, -2*BLIT_OFFSET))
        self.coordinates = coordinates
        tiles.update({coordinates: Tile})
        
    def update_terrain(self, terrain: str):
        self.terrain = terrain
        self.image = terrains[terrain]

    def is_clicked(self):
        mouse_pos = pg.mouse.get_pos()
        return pg.mouse.get_pressed()[0] and self.rect.collidepoint(mouse_pos)

#functions
def new_tile(coordinates: tuple[int,int,int]):
    return tile

def get_screen_pos(coordinates: tuple[int,int,int]) -> np.ndarray:
    return coordinates[0] * AXIS_VECTORS[0] + coordinates[1] * AXIS_VECTORS[1] + coordinates[2] * AXIS_VECTORS[2] + ORIGIN

def get_coordinates(screen_pos: tuple[int, int]) -> np.ndarray:
    pass

def save_tile(tile: Tile):
    tiles.update({tuple(tile.coordinates): Tile})

#organize later
unfilled_tiles = pg.sprite.Group()    
filled_tiles = pg.sprite.Group()

image_path = os.path.join(config.TEXTURE_DIRECTORY, WHITE_TILE_NAME)
white_tile = pg.image.load(image_path)
image_path = os.path.join(config.TEXTURE_DIRECTORY, GREEN_TILE_NAME)
green_tile = pg.image.load(image_path)
image_path = os.path.join(config.TEXTURE_DIRECTORY, DARK_TILE_NAME)
dark_tile = pg.image.load(image_path)

terrains = {
    "unexplored": dark_tile,
    "plains": green_tile,
    "arctic": white_tile
}

display = pg.display.set_mode((0,0),pg.WINDOWMAXIMIZED)
ORIGIN = np.array((display.get_width() // 2, display.get_height() // 2))

tiles = {

}

adjacency_list = (
    np.array((1, -1, 0)),
    np.array((0, -1, 1)),
    np.array((-1, 0, 1)),
    np.array((-1, 1, 0)),
    np.array((0, 1, -1)),
    np.array((1, 0, -1))
)

#main
Tile((0,0,0))
unfilled_tiles.draw(display)
pg.display.flip()

while True:
    events = pg.event.get()
    for tile in unfilled_tiles:
        if tile.is_clicked():
            tile.update_terrain("plains")
            unfilled_tiles.remove(tile)
            filled_tiles.add(tile)  

            for vector in adjacency_list:
                new_pos = tuple(tile.coordinates + vector)
                if (new_pos not in list(tiles.keys()) and new_pos[0] + new_pos[1] + new_pos[2] == 0):
                    Tile(new_pos)

            unfilled_tiles.draw(display)
            filled_tiles.draw(display)
            pg.display.flip()