# camiregu
# 2023-mar-28
import cartographer.tile_manager as tm
import cartographer.display_controller as dc
import cartographer.map_painter as mp
import cartographer.terrain_generator as tg

import pygame as pg
import numpy as np

# functions
def process_user_input() -> bool:
    events = pg.event.get()
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                return True
            
            if event.key == pg.K_f:
                dc.toggle_fullscreen()
                dc.draw_screen()
            
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                # convert mouse position to its equivalent position on the draw_screen
                relative_pos = (pg.mouse.get_pos() - dc.get_blit_position()) * (dc.draw_surface.get_height() // dc.display_surface.get_height()) // dc.scale
                for tile in tm.unfilled:
                    if tile.mouse_is_over(relative_pos):
                        terrain = tg.assign_terrain(tile.coordinates)
                        mp.fill_tile(tile, terrain)
                        dc.draw_screen()

        elif event.type == pg.MOUSEWHEEL:
            dc.scale_display(event.y)
            dc.draw_screen()
    
    return False