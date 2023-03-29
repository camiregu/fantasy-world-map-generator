#camiregu
#2023-mar-28
import cartographer.tile_manager as tm
import cartographer.display_controller as dc
import cartographer.map_painter as mp
import cartographer.terrain_generator as tg

import pygame as pg

#functions
def process_user_input() -> bool: #move
    events = pg.event.get()
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                return True
            
            if event.key == pg.K_f:
                dc.toggle_fullscreen()
            
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("click")
                for tile in tm.unfilled:
                    if tile.mouse_is_over():
                        terrain = tg.assign_terrain(tile.coordinates)
                        mp.fill_tile(tile, terrain)

        elif event.type == pg.MOUSEWHEEL:
            dc.change_scale(event.y)
    
    dc.draw_screen()
    return False