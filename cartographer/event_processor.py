#camiregu
#2023-mar-28
import cartographer.tile_manager as tm
import cartographer.map_painter as mp
import cartographer.terrain_generator as tg

import pygame as pg

#functions
def process_user_input() -> bool: #move
    events = pg.event.get()
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 2:
            pg.quit()
            return True
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for tile in tm.unfilled:
                if tile.mouse_is_over():
                    terrain = tg.assign_terrain(tile.coordinates)
                    mp.fill_tile(tile, terrain)
    
    pg.display.flip()
    return False