# camiregu
# 2023-mar-24
import config
import cartographer.tile_manager as tm

import pygame as pg
import numpy as np


# functions
def start_map(draw_surface: pg.Surface):
    # constants
    global SURFACE, ORIGIN, BLIT_OFFSET, RECT_SIZE, AXIS_VECTORS

    SURFACE = draw_surface
    ORIGIN = np.array((SURFACE.get_width() // 2, SURFACE.get_height() // 2))
    BLIT_OFFSET = ((-2 / np.sqrt(3)) * config.INCIRCLE_RADIUS)
    RECT_SIZE = -2*BLIT_OFFSET, -2*BLIT_OFFSET
    AXIS_VECTORS = (
        np.array((-1/2, -np.sqrt(3)/2)) * (2/np.sqrt(3)) * config.INCIRCLE_RADIUS,
        np.array((-1/2, np.sqrt(3)/2)) * (2/np.sqrt(3)) * config.INCIRCLE_RADIUS,
        np.array((1,0)) * (2/np.sqrt(3)) * config.INCIRCLE_RADIUS
    )

    # draw loaded map
    for tile in tm.tiles.values():
        tile.rect = pg.Rect(get_screen_pos(tile.coordinates) + BLIT_OFFSET, RECT_SIZE)
    set_tiles = tuple(tm.tiles.values())
    for tile in set_tiles:
        surround_tile(tile)
    tm.filled.draw(SURFACE)
    tm.unfilled.draw(SURFACE)
    return


def fill_tile(tile: tm.Tile, terrain: str):
    tile.update_terrain(terrain)
    tile.set_explored(True) 
    surround_tile(tile)
    tm.filled.draw(SURFACE)
    tm.unfilled.draw(SURFACE)
    return


def surround_tile(tile: tm.Tile):
    for vector in config.BASIS_VECTORS:
        pos_1 = tuple(tile.coordinates + np.array(vector))
        if (pos_1 not in list(tm.tiles.keys())):
            new_tile = tm.Tile(pos_1)
            new_tile.rect = pg.Rect(get_screen_pos(new_tile.coordinates) + BLIT_OFFSET, RECT_SIZE)
        pos_2 = tuple(tile.coordinates - np.array(vector))
        if (pos_2 not in list(tm.tiles.keys())):
            new_tile = tm.Tile(pos_2)
            new_tile.rect = pg.Rect(get_screen_pos(new_tile.coordinates) + BLIT_OFFSET, RECT_SIZE)
    return


def get_screen_pos(coordinates: tuple[int,int,int]) -> np.ndarray:
    return coordinates[0] * AXIS_VECTORS[0] + coordinates[1] * AXIS_VECTORS[1] + coordinates[2] * AXIS_VECTORS[2] + ORIGIN